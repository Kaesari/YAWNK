from django.contrib import admin
from .models import HomeGrownBanners, Product, ProductImage, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'reviewer', 'rating', 'timestamp', 'seller_response')
    search_fields = ('product__name', 'reviewer__username')
    list_filter = ('rating', 'timestamp')

from .models import Category,Banners

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')  # Customize the fields you want to display in the admin list view
    search_fields = ('name',)  # Allow search by category name 

@admin.register(HomeGrownBanners)
class HomeGrownBannersAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'image')  # Customize the fields you want to display in the admin list view
    search_fields = ('category',)  # Allow search by category name 

    # 1-left-slide,2-right-slide,3-right-slide (This is how the slides flow)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'target')  # Customize the fields you want to display in the admin list view
    search_fields = ('name',)  # Allow search by category name
    list_filter = ('target',) 

# Register the Product model
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4  # Number of empty form rows to display in the admin for new images

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category','target', 'status','section', 'size','seller')
    search_fields = ['name', 'category', 'status', 'seller__username']  # Add searchable fields
    list_filter = ['category', 'size', 'status', 'brand', 'color', 'condition', 'seller']  # Filters for admin panel

    inlines = [ProductImageInline]  # Add ProductImage inline to Product admin

    # Allow editing the status directly in the list view
    list_editable = ['status']


# Optionally, register the ProductImage model as well
admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
