from django import forms
from admin_panel.models import Category, District, Gifts,Product, Regions,Text



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

class GiftsForm(forms.ModelForm):
    class Meta:

        model = Gifts
        fields = ["name_uz","name_ru","ball"]
        widgets = {
            'name_uz': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'ball': forms.NumberInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }

class RegionsForm(forms.ModelForm):
    class Meta:

        model = Regions
        fields = '__all__'
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }


class DistrictForm(forms.ModelForm):
    class Meta:

        model = District
        fields = '__all__'
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['uz_data','ru_data']
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control col-md-6",
                
                }),
        }