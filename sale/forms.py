from django import forms
from admin_panel.models import Product
from sale.models import SaleDiller

from sale.models import Car, PromoCode, PromocodeRequest, SaleSeller


class PromoCodeForm(forms.ModelForm):
    # diller = forms.ModelChoiceField(queryset=Diller.objects.all())
    # car = forms.ModelChoiceField(queryset=Car.objects.all())

    # order = forms.IntegerField()
    # seria = forms.TextInput()
    # letter = forms.TextInput()
    # code = forms.IntegerField()

    class Meta:
        model = PromoCode
        fields = '__all__'
        # widgets = {
        #     'diller': forms.ModelChoiceField(queryset=Diller.objects.all(),),

        # }


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'


class SaleSellerForm(forms.ModelForm):
    # diller = forms.ModelChoiceField(queryset=Diller.objects.all())
    # car = forms.ModelChoiceField(queryset=Car.objects.all())

    # order = forms.IntegerField()
    # seria = forms.TextInput()
    # letter = forms.TextInput()
    # code = forms.IntegerField()

    class Meta:
        model = SaleSeller
        fields = '__all__'
        # widgets = {
        #     'diller': forms.ModelChoiceField(queryset=Diller.objects.all(),),

        # }



class SaleDillerForm(forms.ModelForm):
    # diller = forms.ModelChoiceField(queryset=Diller.objects.all())
    # car = forms.ModelChoiceField(queryset=Car.objects.all())

    # order = forms.IntegerField()
    # seria = forms.TextInput()
    # letter = forms.TextInput()
    # code = forms.IntegerField()

    class Meta:
        model = SaleDiller
        fields = '__all__'
        # widgets = {
        #     'diller': forms.ModelChoiceField(queryset=Diller.objects.all(),),

        # }



class PromocodeRequestForm(forms.ModelForm):

    class Meta:
        model = PromocodeRequest
        fields = '__all__'




