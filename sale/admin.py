from django.contrib import admin
from sale.models import Car, SaleSeller, Card, SerialNumbers, CashOrder, Cashback,PromoCode
# Register your models here.


admin.site.register(SaleSeller)
admin.site.register(Card)
admin.site.register(SerialNumbers)
admin.site.register(CashOrder)
admin.site.register(Cashback)
admin.site.register(PromoCode)
admin.site.register(Car)
