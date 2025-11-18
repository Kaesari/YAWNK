from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('account/settings/', views.update_user_data, name='account_settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('follow/<int:user_id>/', views.follow_seller_toggle, name='follow_seller_toggle'),
        # Follow toggle action for the seller of a product
    path('follow_toggle/<int:user_id>/<int:product_id>/', views.follow_toggle, name='follow_toggle'),
    path('sellers/', views.seller_list, name='seller_list'),
    path('users/all', views.user_list, name='user_list'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    



]
