from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from accounts.models import CustomUser
from .models import Conversation, Message
from products.models import Product

@login_required
def start_chat(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = product.seller
    buyer = request.user

    # Prevent chatting with self
    if seller == buyer:
        return redirect('product_list')

    # Check if conversation exists
    conversation, created = Conversation.objects.get_or_create(
        buyer=buyer,
        seller=seller,
        product=product
    )
    return redirect('chat_detail', conversation_id=conversation.id)

@login_required
def chat_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in [conversation.buyer, conversation.seller]:
        return redirect('product_list')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            return redirect('chat_detail', conversation_id=conversation.id)

    messages = conversation.messages.order_by('timestamp')
    conversations = Conversation.objects.filter(
        models.Q(buyer=request.user) | models.Q(seller=request.user)
    ).order_by('-started_at')

    return render(request, 'chat/chat_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'conversations': conversations  # Include the conversation list in the context
    })


@login_required
def my_chats(request):
    user = request.user
    q = request.GET.get('q', '')
        
    conversations = Conversation.objects.filter(
        models.Q(buyer=user) | models.Q(seller=user)
    ).order_by('-started_at')

        # If there's a search query, filter conversations by product name, buyer, or seller username
    if q:
        conversations = conversations.filter(
            models.Q(product__name__icontains=q) |
            models.Q(buyer__username__icontains=q) |
            models.Q(seller__username__icontains=q)
        )

    return render(request, 'chat/chat_detail.html', {
        'conversations': conversations,
        'conversation': None,  # Passing None for now, will be set in chat_detail
        'messages': []  # No messages yet, will be populated in chat_detail
    })

