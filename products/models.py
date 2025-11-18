from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify
import os
from django.core.validators import MinValueValidator, MaxValueValidator

CATEGORY_CHOICES = [
    ('Tops', 'Tops'),
    ('Bottoms', 'Bottoms'),
    ('Shoes', 'Shoes'),
    ('Accessories', 'Accessories'),
    ('Dresses', 'Dresses'),
    ('Jackets', 'Jackets'),
    ('Outerwear', 'Outerwear'),
    ('Sweaters', 'Sweaters'),
    ('T-shirts', 'T-shirts'),
    ('Jeans', 'Jeans'),
    ('Shorts', 'Shorts'),
    ('Skirts', 'Skirts'),
    ('Suits', 'Suits'),
    ('Activewear', 'Activewear'),
    ('Sleepwear', 'Sleepwear'),
    ('Swimwear', 'Swimwear'),
    ('Lingerie', 'Lingerie'),
    ('Hats', 'Hats'),
    ('Bags', 'Bags'),
    ('Scarves', 'Scarves'),
    ('Belts', 'Belts'),
    ('Gloves', 'Gloves'),
    ('Socks', 'Socks'),
    ('Jewelry', 'Jewelry'),
    ('Eyewear', 'Eyewear'),
    ('Footwear', 'Footwear'),
    ('Kids', 'Kids'),
    ('Maternity', 'Maternity'),
]

SECTION_CHOICES = [
    ('HomeGrown', 'HomeGrown'),
    ('NewArrival', 'NewArrival'),
    ('StaffPick', 'StaffPick'),
    ('General', 'General'),
]

TARGET_CHOICES = [
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Kids', 'Kids'),
    ('General', 'General'),
]

SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('General', 'General'),
]

CONDITION_CHOICES = [
    ('New', 'New'),
    ('Used', 'Used'),
    ('Fair', 'Fair'),
    ('Good', 'Good'),
    ('Very good', 'Very good'),
    ('New with tags', 'New with tags'),
]

BRAND_CHOICES = [
    ('Nike', 'Nike'),
    ('Adidas', 'Adidas'),
    ('Puma', 'Puma'),
    ('Reebok', 'Reebok'),
    ('Under Armour', 'Under Armour'),
    ('Levi\'s', 'Levi\'s'),
    ('General', 'General'),
    # Add more brands here
]

COLOR_CHOICES = [
    ('Black', 'Black'),
    ('White', 'White'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Yellow', 'Yellow'),
    # Add more colors here
    ('Pink', 'Pink'),
    ('Purple', 'Purple'),
    ('Orange', 'Orange'),
    ('Grey', 'Grey'),
    ('Multicolor', 'Multicolor'),
    ('General', 'General'),
]

# Define the choices for the status field
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class Banners(models.Model):
    name = models.CharField(max_length=100,)  # Name of the category
    image = models.ImageField(upload_to='banner_images/')  # Category image
    title = models.CharField(max_length=100, blank=True, null=True)  # Name of the category
    description = models.CharField(max_length=200, blank=True, null=True)  # Name of the category

    def __str__(self):
        return self.name
    
class HomeGrownBanners(models.Model):
    category = models.CharField(max_length=100,)  # Name of the category
    buttontext = models.CharField(max_length=200,)  # Name of the category
    image = models.ImageField(upload_to='banner_images/')  # Category image
    title = models.CharField(max_length=100, blank=True, null=True)  # Name of the category
    description = models.CharField(max_length=200, blank=True, null=True)  # Name of the category
    slide_direction = models.CharField(
        max_length=10,
        choices=[('left', 'Slide from left'), ('right', 'Slide from right')],
        default='right',
        help_text="Animation direction when this slide appears"
    )

    def __str__(self):
        return self.category
    
class Category(models.Model):
    name = models.CharField(max_length=100,)  # Name of the category
    image = models.ImageField(upload_to='category_images/')  # Category image
    target = models.CharField(max_length=50, choices=TARGET_CHOICES)  # Target audience for the category

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    # category_list = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to Category
    subcategory = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    target = models.CharField(max_length=50, choices=TARGET_CHOICES)
    section = models.CharField(max_length=50,default='General',choices=SECTION_CHOICES)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
        # Add the status field
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending',  # Default to 'Pending'
    )

    def __str__(self):
        return self.name
    
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

def product_image_upload_to(instance, filename):
    """
    Custom function to create a valid file path.
    Slugifies the original filename to ensure the path is valid.
    """
    # Generate a slugified version of the filename
    base, ext = os.path.splitext(filename)
    slugified_name = slugify(base)
    return f"product_images/{slugified_name[:100]}{ext}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_to)
    alt_text = models.CharField(max_length=255, blank=True, null=True, default="Fashion product image")

    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])    
    seller_response = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'reviewer')  # One review per user per product

    def __str__(self):
        return f'{self.reviewer.username} - {self.product.name} ({self.rating}★)'
