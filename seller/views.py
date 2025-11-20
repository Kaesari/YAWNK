from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from products.models import Product
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
import json


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'seller/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all products for this seller
        seller_products = Product.objects.filter(seller=user)
        
        # Calculate statistics from database (REAL DATA)
        # Active Listings: Count products with status='active'
        active_count = Product.objects.filter(seller=self.request.user, status='active').count()
        
        # Items Sold: Count products with status='sold'
        sold_count = Product.objects.filter(seller=self.request.user, status='sold').count()
        
        # Total Revenue: Sum of sold item prices
        revenue_total = Product.objects.filter(seller=self.request.user, status='sold').aggregate(
            total=Sum('price')
        )['total'] or 0
        
        # Pending Shipments: Set to 0 for now (Requires Order model)
        pending_shipments = 0
        
        # ====================================
        # EARNINGS TAB - REAL SALES PERFORMANCE
        # ====================================
        
        # Get today's date
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        # Calculate earnings for different time periods
        # Total Earnings: Sum of all sold items (matches Overview tab)
        earned_total = revenue_total
        
        # Earned Today: Sum of items sold today
        earned_today = Product.objects.filter(
            seller=self.request.user,
            status='sold',
            updated_at__date=today
        ).aggregate(total=Sum('price'))['total'] or 0
        
        # Earned This Week: Sum of items sold in last 7 days
        earned_week = Product.objects.filter(
            seller=self.request.user,
            status='sold',
            updated_at__date__gte=week_ago
        ).aggregate(total=Sum('price'))['total'] or 0
        
        # ====================================
        # GENERATE CHART DATA (Last 7 Days)
        # ====================================
        
        daily_labels = []
        daily_earnings = []
        
        # Loop through last 7 days (from 6 days ago to today)
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            
            # Get day name (Mon, Tue, etc.)
            day_name = date.strftime('%a')
            daily_labels.append(day_name)
            
            # Calculate earnings for this specific day
            day_total = Product.objects.filter(
                seller=self.request.user,
                status='sold',
                updated_at__date=date
            ).aggregate(total=Sum('price'))['total'] or 0
            
            daily_earnings.append(float(day_total))
        
        # Pass data to template
        context['seller_products'] = seller_products
        context['active_count'] = active_count
        context['sold_count'] = sold_count
        context['pending_shipments'] = pending_shipments
        context['total_revenue'] = revenue_total
        
        # Earnings tab data
        context['earned_total'] = earned_total
        context['earned_today'] = earned_today
        context['earned_week'] = earned_week
        context['daily_labels'] = json.dumps(daily_labels)  # Convert to JSON for JS
        context['daily_earnings'] = json.dumps(daily_earnings)  # Convert to JSON for JS
        
        # Keep backward compatibility
        context['available_balance'] = revenue_total * 0.7  # 70% available
        context['pending_clearance'] = revenue_total * 0.3  # 30% pending
        
        return context
