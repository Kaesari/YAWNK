
from django.shortcuts import render, redirect
from django.contrib.auth import login

from products.models import Banners, Category, HomeGrownBanners, Product

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileDetailsForm, AccountDetailsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from django.db.models import Q

from .models import SiteConfiguration

def site_config(request):
    return {
        'site_config': SiteConfiguration.load()
    }

def home_view(request):
    # Define followed_sellers to prevent UnboundLocalError
    followed_sellers = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Now safely access the followers attribute if the user is authenticated
        followed_sellers = request.user.followers.all()

        # Check if the user is not a superuser
        if not request.user.is_superuser:
            # Execute the query if the user is not a superuser
            HomeGrownProducts = Product.objects.filter(status='Approved').filter(section='HomeGrown').order_by('-date_posted')
            NewArrivalProducts = Product.objects.filter(status='Approved').filter(section='NewArrival').order_by('-date_posted')
            StaffPickProducts = Product.objects.filter(status='Approved').filter(section='StaffPick').order_by('-date_posted')
            UserFeedsProducts = Product.objects.filter(status='Approved').filter(seller__in=followed_sellers).order_by('-date_posted')
        else:
            # If the user is a superuser, you can provide all products or some other logic
            HomeGrownProducts = Product.objects.filter(section='HomeGrown').order_by('-date_posted')
            NewArrivalProducts = Product.objects.filter(section='NewArrival').order_by('-date_posted')
            StaffPickProducts = Product.objects.filter(section='StaffPick').order_by('-date_posted')
            UserFeedsProducts = Product.objects.filter(seller__in=followed_sellers).order_by('-date_posted')
    
    else:
        # Handle the case where the user is not logged in (anonymous user)
        HomeGrownProducts = Product.objects.filter(status='Approved').filter(section='HomeGrown').order_by('-date_posted')
        NewArrivalProducts = Product.objects.filter(status='Approved').filter(section='NewArrival').order_by('-date_posted')
        StaffPickProducts = Product.objects.filter(status='Approved').filter(section='StaffPick').order_by('-date_posted')
        UserFeedsProducts = Product.objects.none()  # No products for anonymous users

    men_categories = Category.objects.filter(target='Men')
    women_categories = Category.objects.filter(target='Women')
    home_banners = Banners.objects.all()
    home_grown_banners = HomeGrownBanners.objects.all()

    return render(request, 'pages/home.html', {
        'HomeGrownProducts': HomeGrownProducts,
        'NewArrivalProducts': NewArrivalProducts,
        'StaffPickProducts': StaffPickProducts,
        'UserFeedsProducts': UserFeedsProducts,
        'men_categories': men_categories,
        'women_categories': women_categories,
        'home_banners': home_banners,
        'home_grown_banners': home_grown_banners,
        'user': request.user
    })

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # We'll create this later
    else:
        form = CustomUserCreationForm()
    # return render(request, 'accounts/signup.html', {'form': form})
    return render(request, 'pages/register.html', {'form': form})

@login_required
def update_user_data(request):
    user = request.user
    
    # Initialize all forms with current user data
    profile_form = ProfileDetailsForm(instance=user)
    account_form = AccountDetailsForm(instance=user)
    password_form = None  # Only instantiate when needed
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'submit_profile' in request.POST:
            # Handle Profile Details Form
            profile_form = ProfileDetailsForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                updated_user = profile_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile details have been updated successfully!')
                return redirect('/account/settings/?tab=profile-details')
            else:
                messages.error(request, 'Please correct the errors in Profile Details.')
        
        elif 'submit_account' in request.POST:
            # Handle Account Details Form
            account_form = AccountDetailsForm(request.POST, instance=user)
            if account_form.is_valid():
                updated_user = account_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your account details have been updated successfully!')
                return redirect('/account/settings/?tab=account-details')
            else:
                messages.error(request, 'Please correct the errors in Account Details.')
        
        elif request.POST.get('form_type') == 'password':
            # Handle Password Change Form
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Keep user logged in
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('/account/settings/?tab=password-security')
            else:
                messages.error(request, 'Please correct the errors in the password form.')

    return render(request, 'pages/profile.html', {
        'profile_form': profile_form,
        'account_form': account_form,
        'password_form': password_form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        # Create a password change form instance, binding it to the data from the request
        form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()  # Save the new password
            update_session_auth_hash(request, form.user)  # Prevent the user from being logged out
            messages.success(request, "Your password was successfully updated!")
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'pages/profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'pages/profile.html', {'user': request.user})

@login_required
def follow_seller_toggle(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user == request.user:
        return redirect('seller_feed', user_id)  # Prevent following self

    if target_user in request.user.followers.all():
        request.user.followers.remove(target_user)
    else:
        request.user.followers.add(target_user)

    return redirect('seller_feed', user_id)

@login_required
def follow_toggle(request, user_id, product_id):
    # Get the target user (the seller)
    target_user = get_object_or_404(CustomUser, id=user_id)

    # Get the product (to redirect back to its detail page after toggling follow status)
    product = get_object_or_404(Product, id=product_id)

    # Prevent following oneself
    if target_user == request.user:
        return redirect('product_detail', product_id=product.id)  # Prevent following self

    # Toggle follow/unfollow status
    if target_user in request.user.followers.all():
        request.user.followers.remove(target_user)
    else:
        request.user.followers.add(target_user)

    # Redirect back to the product detail page
    return redirect('product_detail', product_id=product.id)

def user_profile(request, user_id):
    user_profile = get_object_or_404(CustomUser, id=user_id)
    is_following = user_profile in request.user.followers.all() if request.user.is_authenticated else False
    return render(request, 'accounts/user_profile.html', {
        'profile_user': user_profile,
        'is_following': is_following
    })

@login_required
def user_list(request):
    # Get all users excluding the logged-in user
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'pages/user_list.html', {'users': users})

@login_required
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # Create the form and populate it with POST data and the user's data
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, 'User information updated successfully!')
            return redirect('user_list')  # Redirect to the list of users after successful update
    else:
        # Preload the user's data into the form
        form = CustomUserChangeForm(instance=user)

    return render(request, 'pages/update_user.html', {'form': form, 'user': user})

def seller_list(request):
    query = request.GET.get('q')
    sellers = CustomUser.objects.filter(is_seller=True)

    if query:
        sellers = sellers.filter(
            Q(username__icontains=query) |
            Q(location__icontains=query)
        )

    following = request.user.followers.all() if request.user.is_authenticated else []

    return render(request, 'accounts/seller_list.html', {
        'sellers': sellers,
        'query': query,
        'following': following
    })


class UserProfileView(TemplateView):
    """
    Public user profile page - Depop style
    Shows user info, stats, and their product listings
    """
    template_name = 'accounts/public_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        
        # Get the profile user or return 404
        profile_user = get_object_or_404(CustomUser, username=username)
        
        # Get all products by this user
        user_products = Product.objects.filter(seller=profile_user).order_by('-date_posted')
        
        # Check if viewing own profile
        is_own_profile = self.request.user.is_authenticated and self.request.user == profile_user
        
        # Check if current user is following this profile
        is_following = False
        if self.request.user.is_authenticated and not is_own_profile:
            is_following = profile_user in self.request.user.followers.all()
        
        # Get follower and following counts
        followers_count = profile_user.following.count()  # People who follow this user
        following_count = profile_user.followers.count()  # People this user follows
        
        # Get liked products (wishlist)
        liked_products = profile_user.wishlist.all()
        
        context.update({
            'profile_user': profile_user,
            'user_products': user_products,
            'is_own_profile': is_own_profile,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'liked_products': liked_products,
            'products_count': user_products.count(),
        })
        
        return context

