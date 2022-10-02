from dataclasses import fields
from django import forms
from admin_panel.models import Category, District, Gifts,Product, Promotion, Regions,Text,BaseProduct
from diller.models import Diller



class CategoryForm(forms.ModelForm):
    class Meta:

        model = Category
        fields = '__all__'
        widgets = {
            'name_uz': forms.TextInput(attrs={
                'class': "form-control",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'name_uz': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'diller_ball': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
            'diller_nasiya_ball': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
            'seller_ball': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
            'price': forms.NumberInput(attrs={
                'class': "form-control "
                
                })
        }

class GiftsForm(forms.ModelForm):
    class Meta:

        model = Gifts
        fields = ["gift_type","name_uz","name_ru","ball","amount"]
        widgets = {
            'gift_type': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible",
                
                }),
            'name_uz': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'ball': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
            'amount': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
        }

class RegionsForm(forms.ModelForm):
    class Meta:

        model = Regions
        fields = '__all__'
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
        }


class DistrictForm(forms.ModelForm):
    class Meta:

        model = District
        fields = '__all__'
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
        }

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['uz_data','ru_data']
        widgets = {
            'uz_data': forms.TextInput(attrs={
                'class': "form-control",
                
                }),
            'ru_data': forms.TextInput(attrs={
                'class': "form-control",
                
                }),
        }
class SoldForm(forms.ModelForm):
    serial = forms.CharField(max_length=100)
    class Meta:
        model = BaseProduct
        fields = ['diller','product','seller']
        widgets = {
            'diller': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible",
                
                }),
            'seller': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible",
                
                }),
            'product': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible",
                
                }),
            'serial': forms.Textarea(attrs={
                'class': "form-control "
                
                })
        }
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            'product': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible"
                
                }),
            'price': forms.NumberInput(attrs={
                'class': "form-control "
                
                }),
            'ball': forms.NumberInput(attrs={
                'class': "form-control "
                
                }),
            'count': forms.NumberInput(attrs={
                'class': "form-control "
                
                }),
            'active': forms.CheckboxInput(attrs={
                'class': "" 
                
                }),
            'description_uz': forms.Textarea(attrs={
                'class': "form-control "
                
                }),
            'description_ru': forms.Textarea(attrs={
                'class': "form-control "
                
                })
        }


class DillerForm(forms.ModelForm):
    class Meta:
        model = Diller
        fields = ["name","number","region","district"]
        widgets = {
            'region': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible"
                
                }),
            'district': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible"
                
                }),
            'name': forms.TextInput(attrs={
                'class': "form-control "
                
                }),
            'number': forms.NumberInput(attrs={
                'class': "form-control "
                
                })
                   }
