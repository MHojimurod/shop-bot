from ctypes import Union
from datetime import datetime
from typing import List
from django.db import models
from admin_panel.models import *


class Diller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=0, choices=(
        (0, "Kutilmoqda"),
        (1, "Qabul qilingan"),
        (2, "Rad etilgan"),
    ))
    balls = models.IntegerField(default=0)

    def get_gift(self, gift):
        return OrderGiftDiller.objects.create(user=self, gift=gift)

    
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    @property
    def busket(self):
        b = Busket.objects.filter(diller=self, is_ordered=False).first()
        return b if b is not None else Busket.objects.create(diller=self)
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""

    def products(self):
        buskets = Busket.objects.filter(diller=self, is_ordered=True)
        d = {}
        for busket in buskets:
            for item in busket.items:
                if item.product.id not in d:
                    d[item.product.id] = {
                        "product": item.product,
                        "count": item.count,
                        "price": item.product.price
                    }
                else:
                    d[item.product.id]["count"] += item.count
        res = []
        for key, value in d.items():
            res.append({
                "product": value["product"],
                "count": value["count"],
                "price": value["price"]
            })
        return res

    def __str__(self):
        return self.name



class Busket(models.Model):
    diller = models.ForeignKey(Diller, on_delete=models.CASCADE)
    status = models.IntegerField(default=0,choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(2,"Yuborilgan"),(3,"Rad etilgan"),(4,"Yetkazib berildi")))

    payment_type = models.IntegerField(choices=((0, "Variant 1"), (1, "Variant 2")), null=True, blank=True)
    ordered_date = models.DateTimeField(null=True, blank=True)

    is_ordered = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    def total_pricee(self):
        return sum([item.total_price for item in self.items])

    def add_product(self, product:Product, count:int) -> "Busket_item":
        item = self.item(product)
        if item:
            item.count = count
            item.save()
        else:
            item = Busket_item.objects.create(busket=self, product=product, count=count)
        return item

    @property
    def items(self) -> "List[Busket_item]":
        return Busket_item.objects.filter(busket=self)
    
    def item(self, product:Product) -> "Busket_item":
        return Busket_item.objects.filter(busket=self, product=product).first()

    def order(self, payment_type:int) -> None:
        self.payment_type = payment_type
        self.ordered_date = datetime.now()
        self.is_ordered = True
        self.save()
    
    def purchase(self) -> int:
        self.is_purchased = True
        balls = 0
        for busket_item in self.items:
            balls += busket_item.product.diller_ball * busket_item.count
        self.save()
        return balls
    
    @property
    def balls(self) -> int:
        res = 0
        now = datetime.now()
        date = now-self.ordered_date
        for busket_item in self.items:
            res += (busket_item.product.diller_ball if date.days
                <= 3 else busket_item.product.diller_nasiya_ball) * busket_item.count    
        return res
    

    
    
class Busket_item(models.Model):
    busket = models.ForeignKey(Busket, on_delete=models.SET_NULL,null=True)
    product:Product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField()
    active = models.BooleanField(default=True)
    def total_price(self):
        return self.product.price * self.count
    
    @property
    def ball(self):
        return self.product.diller_ball * self.count



class OrderGiftDiller(models.Model):
    user = models.ForeignKey(Diller, on_delete=models.SET_NULL,null=True)
    gift = models.ForeignKey(Gifts, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(3,"Rad etilgan")),default=0)