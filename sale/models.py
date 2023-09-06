from django.db import models
from seller.models import Regions


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

    def __str__(self):
        return self.name

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
    def __str__(self):
        return f"{self.code} | {self.cashback} {self.is_used} | {self.seller}"
    
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