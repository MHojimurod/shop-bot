from django import forms
from admin_panel.models import Product
from diller.models import Diller
from sale.models import Car, PromoCode


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
    # diller = forms.ModelChoiceField(queryset=Diller.objects.all())
    # car = forms.ModelChoiceField(queryset=Car.objects.all())

    # order = forms.IntegerField()
    # seria = forms.TextInput()
    # letter = forms.TextInput()
    # code = forms.IntegerField()

    class Meta:
        model = Car
        fields = '__all__'
        # widgets = {
        #     'diller': forms.ModelChoiceField(queryset=Diller.objects.all(),),

        # }


