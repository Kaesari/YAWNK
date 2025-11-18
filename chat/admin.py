from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'product', 'started_at')
    search_fields = ('buyer__username', 'seller__username', 'product__name')
    inlines = [MessageInline]

admin.site.register(Conversation, ConversationAdmin)
