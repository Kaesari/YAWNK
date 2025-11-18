from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_product, name='create_product'),
    path('', views.product_list, name='product_list'),
    path('feed/', views.user_feed, name='user_feed'),
    path('sellerfeeds/<int:seller_id>/', views.seller_feed, name='seller_feed'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/delete-review/', views.delete_review, name='delete_review'),
    path('listing/', views.all_product_list, name='listing_settings'),
    path('update/<int:id>/', views.update_product, name='update_product'),
    path('update-status/<int:product_id>/', views.update_product_status, name='update_product_status'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]
