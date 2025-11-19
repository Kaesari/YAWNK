from django.contrib import admin
from django.utils.html import format_html
from .models import CaptainViceCaptainHistory, Contest, MpesaPayment, Player, Team, UserProfile

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'entry_fee', 'prize_pool', 'gameweek', 'start_date')
    search_fields = ('name', 'sport',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'name', 'score', 'position', 'team','gameweek','image_preview')  # Add image_preview column
    search_fields = ('name', 'team', 'position', 'gameweek',)
    list_filter = ('gameweek',)

    def image_preview(self, obj):
        """Display player's image in the Django Admin panel."""
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.image_url)
        return "No Image"
    
    image_preview.short_description = "Player Image"  # Custom column name

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name','captain','vice_captain')

@admin.register(CaptainViceCaptainHistory)
class CaptainViceCaptainHistoryAdmin(admin.ModelAdmin):
    list_display = ('team', 'captain', 'vice_captain', 'gameweek', 'date_assigned')  # Customize the columns to show
    search_fields = ('team__name', 'captain__name', 'vice_captain__name')  # Add search fields
    list_filter = ('gameweek',)  # Optionally add filters for gameweek

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('checkout_request_id', 'status', 'amount', 'phone', 'created_at')
    search_fields = ('checkout_request_id', 'phone')
    list_filter = ('status', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'day', 'month', 'year', 'country', 'phone_number')
    search_fields = ('user__username', 'phone_number', 'country')

