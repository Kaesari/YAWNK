from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from contests.models import Contest, Team
from django.db.models import Sum, Q

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth_url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    r.raise_for_status()
    return r.json().get('access_token')

def mpesa_b2c_payout(phone_number, amount, remarks="Payout", occasion="Winner"):
    access_token = get_mpesa_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "InitiatorName": settings.MPESA_INITIATOR_NAME,
        "SecurityCredential": settings.MPESA_B2C_SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",  # or "PromotionPayment" or "SalaryPayment"
        "Amount": int(amount),
        "PartyA": settings.MPESA_B2C_SHORTCODE,
        "PartyB": phone_number,
        "Remarks": remarks,
        "QueueTimeOutURL": settings.MPESA_B2C_TIMEOUT_URL,
        "ResultURL": settings.MPESA_B2C_RESULT_URL,
        "Occasion": occasion,
    }
    url = f"{settings.MPESA_BASE_URL}/mpesa/b2c/v1/paymentrequest"
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

@csrf_exempt
def mpesa_b2c_result(request):
    data = json.loads(request.body.decode('utf-8'))
    # Log or process payout result here
    # Example: Save to database or update payout status
    print("B2C Result Callback:", data)
    return HttpResponse("OK")

@csrf_exempt
def mpesa_b2c_timeout(request):
    data = json.loads(request.body.decode('utf-8'))
    # Log or process timeout here
    print("B2C Timeout Callback:", data)
    return HttpResponse("OK")

# Example usage in your payout logic:
# from .payouts import mpesa_b2c_payout
# result = mpesa_b2c_payout(winner_phone, amount, remarks="League Winnings")

from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def payout_winner(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        if not phone_number or not amount:
            return JsonResponse({'error': 'phone_number and amount are required'}, status=400)
        result = mpesa_b2c_payout(phone_number, amount, remarks="League Winnings")

        # print("Payout Result:", result)  # Log the payout result for debugging
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def payout_league_winners_70_percent_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        league_code = data.get('league_code')
        if not league_code:
            return JsonResponse({'error': 'league_code is required'}, status=400)
        result = payout_league_winners_70_percent(league_code)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def payout_all_league_winners_for_gameweek(gameweek):
    from .models import Contest
    results = []
    leagues = Contest.objects.filter(gameweek=gameweek)
    for league in leagues:
        if getattr(league, 'payout_sent', False):
            results.append({
                "league": league.name,
                "league_code": league.league_code,
                "status": "Payout already sent"
            })
            continue
        from .payouts import payout_league_winners_70_percent
        payout_result = payout_league_winners_70_percent(league.league_code)
        results.append({
            "league": league.name,
            "league_code": league.league_code,
            "payout_result": payout_result
        })
    return results

def payout_league_winners_70_percent(league_code):
    contest = get_object_or_404(Contest, league_code=league_code)
    league_users = contest.users.all()
    gameweek = contest.gameweek

    # Get teams and their total scores for the league's gameweek
    teams = Team.objects.filter(user__in=league_users).annotate(
        total_score=Sum('players__score', filter=Q(players__gameweek=gameweek))
    ).order_by('-total_score')

    if not teams.exists():
        return {"error": "No teams found for this league."}

    # Find the highest score
    highest_score = teams.first().total_score
    # Find all teams with the highest score (handle ties)
    winning_teams = teams.filter(total_score=highest_score)
    num_winners = winning_teams.count()
    if num_winners == 0:
        return {"error": "No winners found."}

    # Calculate 70% of the prize pool to be shared among winners
    payout_amount = float(contest.prize_pool) * 0.7
    share = payout_amount / num_winners

    results = []
    for team in winning_teams:
        winner_user = team.user
        profile = getattr(winner_user, 'profile', None)
        if profile is None or not profile.phone_number:
            results.append({"winner": winner_user.username, "status": "No phone number or profile"})
            continue
        phone_number = profile.phone_number
        payout_result = mpesa_b2c_payout(phone_number, share, remarks=f"70% Payout for winning {contest.name}")
        results.append({
            "winner": winner_user.username,
            "phone": phone_number,
            "amount": share,
            "payout_result": payout_result
        })

    # Optionally, mark the league as paid out
    contest.payout_sent = True
    contest.save()

    # Host keeps 30% (you can log or process this as needed)
    host_share = float(contest.prize_pool) * 0.3

    return {
        "winners": results,
        "host_share": host_share,
        "total_payout": payout_amount,
        "prize_pool": float(contest.prize_pool)
    }