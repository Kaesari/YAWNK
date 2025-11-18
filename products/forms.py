from django import forms
from .models import Product, ProductImage
from .models import Review



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'size', 'condition', 'brand', 'subcategory', 'target', 'section', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description', 'rows': 3, 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'size': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'condition': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'brand': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'color': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'required'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'target': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'section': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)],  # Using stars instead of numbers
                attrs={'class': 'd-flex flex-row gap-3'}  # Add this line
            ),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'What did you like or dislike? What did you use this product for?'
            }),
        }

class SellerResponseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['seller_response']
        widgets = {
            'seller_response': forms.Textarea(attrs={'rows': 3}),
        }

