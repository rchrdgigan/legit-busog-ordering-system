from django import forms
from .models import ProductInfo


class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ('image',)
