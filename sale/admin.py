from django.contrib import admin
from sale.models import SaleSeller, Card, SerialNumbers, CashOrder, Cashback
# Register your models here.


admin.site.register(SaleSeller)
admin.site.register(Card)
admin.site.register(SerialNumbers)
admin.site.register(CashOrder)
admin.site.register(Cashback)