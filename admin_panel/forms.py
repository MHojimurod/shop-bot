from statistics import mode
from django import forms
from admin_panel.models import Category,Product



class CategoryForm(forms.ModelForm):
    class Meta:

        model = Category
        fields = '__all__'
        widgets = {
            'name_uz': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'name_uz': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'ball': forms.NumberInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'price': forms.NumberInput(attrs={
                'class': "form-control col-md-6"
                
                }), 
            'serial_number': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }
