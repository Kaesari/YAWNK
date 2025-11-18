from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from products.models import Product

class Conversation(models.Model):
    buyer = models.ForeignKey(CustomUser, related_name='conversations_started', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='conversations_received', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Chat about {self.product.name} between {self.buyer.username} & {self.seller.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
