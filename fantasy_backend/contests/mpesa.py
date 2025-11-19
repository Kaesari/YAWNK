import base64
from django.shortcuts import render
import requests
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import MpesaPayment, Contest

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth_url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    return r.json().get('access_token')

def get_mpesa_password():
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    encoded = base64.b64encode(data_to_encode.encode()).decode()
    return encoded, timestamp

def initiate_mpesa_stk_push(phone_number, amount, account_reference, transaction_desc):
    callback_url = settings.MPESA_CALLBACK_URL
    access_token = get_mpesa_access_token()
    password, timestamp = get_mpesa_password()
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }
    url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@csrf_exempt
@require_POST
def mpesa_callback(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        body = data['Body']['stkCallback']
        checkout_request_id = body['CheckoutRequestID']
        result_code = body['ResultCode']
        result_desc = body['ResultDesc']
        amount = None
        phone = None
        if result_code == 0:
            for item in body['CallbackMetadata']['Item']:
                if item['Name'] == 'Amount':
                    amount = item['Value']
                if item['Name'] == 'PhoneNumber':
                    phone = item['Value']
            MpesaPayment.objects.update_or_create(
                checkout_request_id=checkout_request_id,
                defaults={
                    'status': 'Success',
                    'amount': amount,
                    'phone': phone,
                    'raw': data,
                }
            )
        else:
            MpesaPayment.objects.update_or_create(
                checkout_request_id=checkout_request_id,
                defaults={
                    'status': 'Failed',
                    'raw': data,
                }
            )
    except Exception as e:
        print("M-Pesa callback error:", e)
    return HttpResponse("OK")

def wait_for_payment(request):
    return render(request, 'contests/wait_for_payment.html')

# def check_payment_status(request):
#     checkout_request_id = request.session.get('mpesa_checkout_request_id')
#     if not checkout_request_id:
#         return JsonResponse({'status': 'not_found'})
#     payment = MpesaPayment.objects.filter(checkout_request_id=checkout_request_id, status='Success').first()
#     if payment:
#         pending_league = request.session.get('pending_league')
#         if pending_league:
#             from .views import create_league_from_pending
#             league = create_league_from_pending(request.user, pending_league)
#             del request.session['pending_league']
#             del request.session['mpesa_checkout_request_id']
#             return JsonResponse({'status': 'success', 'redirect_url': reverse('payment-success', args=[league.id])})
#     return JsonResponse({'status': 'pending'})


def check_payment_status(request):
    checkout_request_id = request.session.get('mpesa_checkout_request_id')
    if not checkout_request_id:
        return JsonResponse({'status': 'not_found'})
    payment = MpesaPayment.objects.filter(checkout_request_id=checkout_request_id).first()
    if payment:
        if payment.status == 'Success':
            pending_league = request.session.get('pending_league')
            if pending_league:
                from .views import create_league_from_pending
                league = create_league_from_pending(request.user, pending_league)
                del request.session['pending_league']
                del request.session['mpesa_checkout_request_id']
                return JsonResponse({'status': 'success', 'redirect_url': reverse('payment-success', args=[league.id])})
        elif payment.status == 'Failed':
            return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'pending'})

def payment_success(request, league_id):
    league = Contest.objects.get(id=league_id)
    return render(request, 'contests/payment_success.html', {'league': league})