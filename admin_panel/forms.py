from django import forms
from admin_panel.models import Category, District, Gifts,Product, Promotion, Regions,Text,BaseProduct



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
            'ball': forms.NumberInput(attrs={
                'class': "form-control ",
                
                }),
            'price': forms.NumberInput(attrs={
                'class': "form-control "
                
                }), 
            'serial_number': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
        }

class GiftsForm(forms.ModelForm):
    class Meta:

        model = Gifts
        fields = ["name_uz","name_ru","ball"]
        widgets = {
            'name_uz': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'name_ru': forms.TextInput(attrs={
                'class': "form-control ",
                
                }),
            'ball': forms.NumberInput(attrs={
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
    class Meta:
        model = BaseProduct
        fields = ['diller','product',"serial_number"]
        widgets = {
            'diller': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible","value":124343
                
                }),
            'product': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible","value":124343
                
                }),
            'serial_number': forms.TextInput(attrs={
                'class': "form-control ","value":124343
                
                })
        }
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            'product': forms.Select(attrs={
                'class': "form-control select2 select2-hidden-accessible","value":124343
                
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