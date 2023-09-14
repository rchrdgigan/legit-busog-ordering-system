from django import forms
from .models import ProductInfo, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('image',)


class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('image',)
