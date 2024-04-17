from django import forms
from admin_panel.models import Product
from sale.models import SaleDiller, SaleSeller2

from sale.models import Car, PromoCode, PromocodeRequest, SaleSeller


class PromoCodeForm(forms.ModelForm):

    class Meta:
        model = PromoCode
        fields = '__all__'


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'


class SaleSellerForm(forms.ModelForm):
    class Meta:
        model = SaleSeller
        fields = '__all__'


class SaleSeller2Form(forms.ModelForm):
    class Meta:
        model = SaleSeller2
        fields = '__all__'



class SaleDillerForm(forms.ModelForm):

    class Meta:
        model = SaleDiller
        fields = '__all__'



class PromocodeRequestForm(forms.ModelForm):

    class Meta:
        model = PromocodeRequest
        fields = '__all__'




