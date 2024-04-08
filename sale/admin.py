from django.contrib import admin
from sale.models import Car, SaleSeller, Card, SerialNumbers, CashOrder, Cashback,PromoCode, UserGift,PromocodeRequest
# Register your models here.


admin.site.register(SaleSeller)
admin.site.register(Card)
admin.site.register(SerialNumbers)
admin.site.register(CashOrder)
admin.site.register(Cashback)
admin.site.register(PromoCode)
admin.site.register(Car)
admin.site.register(PromocodeRequest)




@admin.register(UserGift)
class UserGiftAdmin(admin.ModelAdmin):
    model = UserGift

    inlines = [
        type(
            "UserGiftPromocodeTabular",
            (admin.TabularInline,),
            {
                "model": PromoCode,
                "extra": 0
            }
        )
    ]



