
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProductForm, ReviewForm, SellerResponseForm, ProductImageForm
from .models import Product, Review, ProductImage
from django.contrib import messages
from django.forms import modelformset_factory

from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .models import Product, ProductImage, Category
from .forms import ProductForm, ProductImageForm
from django.contrib.auth.decorators import login_required
import os


from django.db.models import Count
from .models import CustomUser
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


@login_required
def create_product(request):
    # if not request.user.is_seller:
    #     return redirect('home')
    
    allProducts = Product.objects.order_by('-date_posted')

    # Define formset for product images
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)

    if request.method == 'POST':
        # Handle product form and image formset submission
        product_form = ProductForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if product_form.is_valid() and image_formset.is_valid():
            # Save product
            product = product_form.save(commit=False)
            product.seller = request.user
            product.save()

            # Save images
            for form in image_formset:
                image = form.cleaned_data.get('image')
                if image:
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        alt_text=form.cleaned_data.get('alt_text') or "Fashion product image"
                    )

            return redirect('product_detail', product_id=product.id)

        print("Product form errors:", product_form.errors)
        print("Image formset errors:", image_formset.errors)

    else:
        product_form = ProductForm()
        image_formset = ImageFormSet(queryset=ProductImage.objects.none())  # Create empty formset for new product

    return render(request, 'pages/create_product.html', {
        'form': product_form,
        'allProducts': allProducts,
        'product_image_formset': image_formset,
    })

@login_required
def update_product(request, id):
    # Fetch the product that needs to be updated
    product = get_object_or_404(Product, id=id, seller=request.user)

    # Define formset for product images
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)

    if request.method == 'POST':
        # Handle product form and image formset submission
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))

        if product_form.is_valid() and image_formset.is_valid():
            # Save product
            product = product_form.save(commit=False)
            product.save()

            # Save images (add or update)
            for form in image_formset:
                image = form.cleaned_data.get('image')
                if image:
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        alt_text=form.cleaned_data.get('alt_text') or "Fashion product image"
                    )

            return redirect('product_detail', product_id=product.id)

        print("Product form errors:", product_form.errors)
        print("Image formset errors:", image_formset.errors)

    else:
        # Prepopulate the form with existing product data
        product_form = ProductForm(instance=product)
        image_formset = ImageFormSet(queryset=ProductImage.objects.filter(product=product))

    return render(request, 'pages/update_product.html', {
        'form': product_form,
        'product_image_formset': image_formset,
        'product': product,
    })

def update_product_status(request, product_id):
    if request.method == 'POST':
        # Get the product
        product = get_object_or_404(Product, id=product_id)
        
        # Update the status field with the selected value
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Approved', 'Rejected']:
            product.status = new_status
            product.save()
            
        # Redirect back to the product list or the product detail page
        return redirect('listing_settings')  # Update with the appropriate URL name

def all_product_list(request):
    if not request.user.is_superuser:   
        allProducts = Product.objects.filter(seller=request.user).order_by('-date_posted')
    else:
        allProducts = Product.objects.order_by('-date_posted')

    return render(request, 'pages/listing_product.html', {
        'allProducts': allProducts,
    })

def product_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    size = request.GET.get('size', '')
    condition = request.GET.get('condition', '')
    brand = request.GET.get('brand', '')  # Get the brand filter from query params
    color = request.GET.get('color', '')  # Get the color filter from query params
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    target = request.GET.get('target', '')  # Get the target filter from query params

    # print(category)
    # print(brand)
    # print(color)

    # Start with all products
    products = Product.objects.all().order_by('-date_posted')

            # Check if the user is not a superuser
    if not request.user.is_superuser:
        # Execute the query if the user is not a superuser
        # allProducts = Product.objects.filter(status='Approved').order_by('-date_posted')
        products = Product.objects.filter(status='Approved').order_by('-date_posted')
    else:
        products = Product.objects.order_by('-date_posted')

    # Apply filters based on query parameters
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if target:
        products = products.filter(target=target)  # Filter by target


    if category:
        products = products.filter(category=category)
    if size:
        products = products.filter(size=size)
    if condition:
        products = products.filter(condition=condition)
    if brand:
        products = products.filter(brand=brand)  # Filter by brand
    if color:
        products = products.filter(color=color)  # Filter by color

    # Apply price filters if provided
    if min_price:
        try:
            min_price = float(min_price)  # Ensure min_price is treated as a number
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass  # Ignore if min_price is not a valid number

    if max_price:
        try:
            max_price = float(max_price)  # Ensure max_price is treated as a number
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass  # Ignore if max_price is not a valid number

    # Handle the "followed" users for the feed view
    if request.user.is_authenticated:
        followed = request.user.followers.all()
    else:
        followed = []

    return render(request, 'pages/product_list.html', {
        'products': products,
        'followed': followed,
        'filters': {
            'query': query,
            'category': category,
            'size': size,
            'condition': condition,
            'brand': brand,  # Add brand to the filters
            'color': color,  # Add color to the filters
            'min_price': min_price,
            'max_price': max_price,
        }
    })

@login_required
def user_feed(request):
    followed_sellers = request.user.followers.all()
    products = Product.objects.filter(seller__in=followed_sellers).order_by('-date_posted')
    return render(request, 'pages/user_feed.html', {'products': products})

@login_required
def seller_feed(request, seller_id):
    # Fetch the specific seller using seller_id
    seller = CustomUser.objects.get(id=seller_id)

    # Fetch the products for this seller
    products = Product.objects.filter(seller=seller).order_by('-date_posted')

    is_following = False
    if request.user.is_authenticated:
        is_following = seller in request.user.followers.all()

    return render(request, 'pages/seller_profile.html', {
        'seller': seller,
        'products': products,
        'is_following': is_following,
    })

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if product in user.wishlist.all():
        user.wishlist.remove(product)
    else:
        user.wishlist.add(product)

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def wishlist_view(request):
    products = request.user.wishlist.all()
    return render(request, 'pages/wishlist.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    review_form = None
    seller_response_form = None
    product_images = product.images.all()
    RelatedProducts = Product.objects.filter(category=product.category).order_by('-date_posted')

    from chat.models import Conversation

    if (
        request.user.is_authenticated and 
        request.user != product.seller and
        Conversation.objects.filter(buyer=request.user, product=product).exists()
    ):

    # if request.user.is_authenticated and request.user != product.seller:
        try:
            existing_review = Review.objects.get(product=product, reviewer=request.user)
        except Review.DoesNotExist:
            existing_review = None

        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=existing_review)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.reviewer = request.user
                review.save()
                return redirect('product_detail', product_id=product.id)
        else:
            review_form = ReviewForm(instance=existing_review)
            
    if request.user.is_authenticated and request.user == product.seller:
        if request.method == 'POST' and 'seller_response' in request.POST:
            response_form = SellerResponseForm(request.POST, instance=existing_review)
            if response_form.is_valid():
                response_form.save()
                return redirect('product_detail', product_id=product.id)
        else:
            seller_response_form = SellerResponseForm()
    # Check if the user is authenticated before checking for followers
    is_following = False
    if request.user.is_authenticated:
        is_following = product.seller in request.user.followers.all()
    
    # print(is_following)

    return render(request, 'pages/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'product_images': product_images,
        'seller_response_form': seller_response_form,
        'RelatedProducts':RelatedProducts,
        'is_following': is_following,
    })

    # return render(request, 'products/product_detail.html', {
    #     'product': product,
    #     'reviews': reviews,
    #     'review_form': review_form,
    # })

@login_required
def delete_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        review = Review.objects.get(product=product, reviewer=request.user)
        review.delete()
        messages.success(request, "Your review has been deleted.")
    except Review.DoesNotExist:
        messages.error(request, "You have no review to delete.")

    return redirect('product_detail', product_id=product.id)

def dashboard_view(request):
    # Fetching data
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()

    # Create the charts using matplotlib
    # Create a simple bar chart
    fig, ax = plt.subplots()
    ax.bar(['Users', 'Products', 'Categories'], [total_users, total_products, total_categories])
    ax.set_ylabel('Count')
    ax.set_title('Summary of Users, Products, and Categories')

    # Save the plot to a BytesIO object to embed it in the HTML page
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    image_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'pages/dashboard.html', {
        'total_users': total_users,
        'total_products': total_products,
        'total_categories': total_categories,
        'image_data': image_data
    })


