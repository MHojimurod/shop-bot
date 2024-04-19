from typing import TYPE_CHECKING
from django.db import models
from admin_panel.models import District
from seller.models import Regions

from django.utils import timezone





class SaleDiller(models.Model):
    name:str = models.CharField(max_length=100)
    number:str = models.CharField(max_length=100)
    region: Regions = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district: District = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)


    promocodes: models.QuerySet["PromoCode"]



    def got_promos(self):
        return self.promocodes.count()

    def used_promos(self):
        return self.promocodes.filter(status=3).count()





class SaleSeller(models.Model):

    WAITING = 1
    CANCELED = -1
    ACCEPT = 2
    chat_id = models.BigIntegerField()
    language = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    state = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.BigIntegerField(default=0)



    ################################
    #          KOMILJONOV          #
    ################################


    diller: "SaleDiller | None" = models.ForeignKey(SaleDiller,on_delete=models.SET_NULL, null=True,blank=True,related_name="sale_sellers")

    last_promocode: "PromoCode" = models.ForeignKey("PromoCode", on_delete=models.SET_NULL,null=True,blank=True)


    gifts: models.QuerySet["UserGift"]
    promocodes: models.QuerySet["PromoCode"]


    ################################
    #        KOMILJONOV END        #
    ################################
    def __str__(self):
        return self.name or ""

    def set_language(self, language):
        self.language = language
        self.save()

    def set_name(self, name):
        self.name = name
        self.save()

    def set_phone(self, phone):
        self.phone = phone
        self.save()

    def set_region(self, region):
        self.region = region
        self.state = self.WAITING
        self.save()

    @property
    def total_sum(self):
        order = Cashback.objects.exclude(state=3).filter(seria__seller=self)
        price = 0
        for i in order:
            price+= i.seria.cashback
        return price

    @property
    def payed_sum(self):
        order = CashOrder.objects.exclude(state=3).filter(seller=self)
        price = 0
        for i in order:
            price+= i.price
        return price
    @property
    def waiting_sum(self):
        cashback = Cashback.objects.filter(seria__seller=self, state=1)
        cashback_price = 0
        for i in cashback:
            cashback_price+= i.seria.cashback
        return cashback_price





    def gifts_text(self, breaker=" <br>"):
        gifts_text = ""

        gifts = self.gifts.all()

        for gift in gifts:
            t = ""
            c_count = {}
            for c in gift.car.name:
                i = c_count.get(c,0) + 1
                promo = gift.promocodes.filter(letter__iexact=c, order=i).first()
                if promo:
                    t += promo.letter
                else:
                    t += "*"

                c_count[c] = i

            gifts_text += t + breaker

        return gifts_text.capitalize()




class SaleSeller2(SaleSeller):
    pass



class Card(models.Model):
    seller = models.ForeignKey(SaleSeller, on_delete=models.CASCADE, null=True)
    holder_name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)


class SerialNumbers(models.Model):
    code = models.CharField(max_length=200)
    cashback = models.IntegerField()
    is_used = models.BooleanField(default=False)
    seller = models.ForeignKey(SaleSeller, on_delete=models.SET_NULL, null=True, blank=True)
    used_time = models.DateTimeField(null=True, blank=True)
    # def __str__(self):
    #     return f"{self.code} | {self.is_used}"

class CashOrder(models.Model):
    WAITING = 1
    ACCEPTED = 2
    CANCELLED = -1

    seller = models.ForeignKey(SaleSeller, on_delete=models.CASCADE)
    price = models.IntegerField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    state = models.SmallIntegerField(default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.name} | {self.state}"


class Cashback(models.Model):
    WAITING = 1
    ACCEPTED = 2
    REJECTED = 3
    photo = models.ImageField(upload_to="cashback/")
    seria = models.ForeignKey(SerialNumbers, on_delete=models.CASCADE, related_name="serialnumber")
    state = models.SmallIntegerField(default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seria.code} | {self.seria.seller.name} | {self.state}"











################################
#          KOMILJONOV          #
################################


class Car(models.Model):
    name = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)


    promocodes: models.QuerySet["PromoCode"]


    def __str__(self) -> str:
        return self.name





# class PromoCode(models.Model):
#     diller: "Diller" = models.ForeignKey("diller.Diller",on_delete=models.SET_NULL,null=True,blank=True)

#     car:Car = models.ForeignKey(Car, on_delete=models.SET_NULL,null=True,blank=True)

#     order = models.IntegerField(default=1)

#     seria = models.CharField(max_length=255)
#     letter = models.CharField(max_length=255)

#     code = models.IntegerField()



class UserGift(models.Model):
    user = models.ForeignKey(SaleSeller2,on_delete=models.CASCADE,related_name="gifts")
    car = models.ForeignKey(Car,on_delete=models.CASCADE)



    promocodes: models.QuerySet["PromoCode"]


class PromoCode(models.Model):
    diller:"SaleDiller" = models.ForeignKey(SaleDiller, on_delete=models.SET_NULL, null=True, blank=True,related_name="promocodes")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True,related_name="promocodes")
    order = models.IntegerField(default=1)
    seria = models.CharField(max_length=255, unique=True)  # Unique individually
    letter = models.CharField(max_length=255)
    code = models.IntegerField(unique=True)  # Unique individually



    status = models.IntegerField(
        choices=[
            (1, "Waiting"),
            (2, "Not used"),
            (3, "Used"),
        ],
        default=1
    )

    seller = models.ForeignKey(SaleSeller2, on_delete=models.SET_NULL,null=True,blank=True,related_name="promocodes")
    image = models.ImageField(upload_to="promocode_images",null=True,blank=True)


    gift = models.ForeignKey(UserGift,on_delete=models.SET_NULL,null=True,blank=True,related_name="promocodes")


    created_at = models.DateTimeField(auto_now_add=True)

    got_at = models.DateTimeField(null=True,blank=True)


    def give_promo(self, request:"PromocodeRequest", db_user:"SaleSeller2"):

        promo = request.promo
        car = promo.car

        gifts = db_user.gifts.filter(car=car)

        for gift in gifts:
            c_count = {}
            for c in gift.car.name.lower():
                i = c_count.get(c,0) + 1

                if c == promo.letter:

                    p = gift.promocodes.filter(letter__iexact=c, order=promo.order).first()
                    if not p:
                        print("Not Found")
                        promo.gift = gift
                        promo.got_at = timezone.now()
                        promo.save()
                        return
                c_count[c] = i

        new_gift = UserGift.objects.create(
            user=db_user,
            car=promo.car
        )
        print("Created")

        promo.gift = new_gift
        promo.save()


    class Meta:
        unique_together = (('car', 'seria', 'letter', 'code'),)  # Unique together

        ordering = ["car", "letter","order"]

    def __str__(self):
        return f"{self.car.name} - {self.letter} - {self.seria} - {self.code}"



    def gifts_text_seller(self, breaker="<br>"):
        gifts_text = ""



        # promos = self.seller.promocodes.order_by("got_at").all()



        gifts = self.seller.gifts.all()


        for gift in gifts:
            t = ""
            c_count = {}
            for c in gift.car.name:
                i = c_count.get(c,0) + 1
                print(c,i,self.got_at)
                promo = gift.promocodes.filter(letter__iexact=c, order=i,got_at__lte=self.got_at).first()
                if promo:
                    t += promo.letter
                else:
                    t += "*"

                c_count[c] = i

            if any([c != "*" for c in t]):
                gifts_text += t + breaker

        return gifts_text













class PromocodeRequest(models.Model):
    seller = models.ForeignKey(SaleSeller2,on_delete=models.CASCADE,related_name="promo_requests")
    promo = models.ForeignKey(PromoCode, on_delete=models.SET_NULL,related_name="promo_requests",null=True,blank=True)

    image = models.ImageField(upload_to="promo_request_images")


    status = models.IntegerField(choices=[
        (1, "Kutilmoqda"),
        (2, "Tasdiqlandi"),
        (3, "Rad etildi"),
    ],default=1)




    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    # changed_by = models.ForeignKey()






################################
#        KOMILJONOV END        #
################################
