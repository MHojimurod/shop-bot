from ctypes import Union
from datetime import datetime
from email.policy import default
from typing import List
from django.db import models
from admin_panel.models import *
from seller.models import Seller


class Diller(models.Model):
    chat_id:int = models.IntegerField(default=0)
    name:str = models.CharField(max_length=100)
    number:str = models.CharField(max_length=100)
    region: Regions = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district: District = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    status:int = models.IntegerField(default=0, choices=(
        (0, "Kutilmoqda"),
        (1, "Qabul qilingan"),
        (2, "Rad etilgan"),
    ))
    balls:int = models.IntegerField(default=0)

    def get_gift(self, gift) -> "OrderGiftDiller":
        return OrderGiftDiller.objects.create(user=self, gift=gift)

    
    language:int = models.IntegerField(default=0,choices=((0, 'uz'), (1, 'ru')))
    @property
    def busket(self) -> "Busket":
        b = Busket.objects.filter(diller=self, is_ordered=False).first()
        return b if b is not None else Busket.objects.create(diller=self)
    
    def text(self, name) -> str:
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""

    def products(self) -> "list[Busket_item]":
        buskets: "list[Busket]" = Busket.objects.filter(diller=self, is_ordered=True)
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

    
    def sellers_count(self,from_date,to_date):
        data = "Seller".objects.filter(diller__in=self,status=1,created_at__date___lte=from_date,created_at__date__gte=to_date)
        balls = 0
        for i in data:
            balls+=i.balls

        active = Seller.objects.filter(diller__in=self,balls__gt=0,status=1,created_at__date___lte=from_date,created_at__date__gte=to_date).count()
        return data.count(), balls, active




class Busket(models.Model):
    diller: Diller = models.ForeignKey(Diller, on_delete=models.CASCADE)
    status:int = models.IntegerField(default=0,choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(2,"Yuborilgan"),(3,"Rad etilgan"),(4,"Yetkazib berildi")))

    payment_type:int = models.IntegerField(choices=((0, "Variant 1"), (1, "Variant 2")), null=True, blank=True)
    ordered_date: datetime = models.DateTimeField(null=True, blank=True)

    is_ordered:bool = models.BooleanField(default=False)
    is_purchased:bool = models.BooleanField(default=False)

    def total_pricee(self) -> int:
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
        balls:int = 0
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
            # res += (busket_item.product.diller_ball if date.days
                # <= 3 else busket_item.product.diller_nasiya_ball) * busket_item.count
                res += busket_item.product.diller_ball * busket_item.count
        return res
    
    def ball_by_var(self, var):
        res = 0
        for busket_item in self.items:
                res += (busket_item.product.diller_ball if var == 1 else busket_item.product.diller_nasiya_ball) * busket_item.count
        return res



class Busket_item(models.Model):
    busket:Busket = models.ForeignKey(Busket, on_delete=models.SET_NULL,null=True)
    product:Product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count:int = models.IntegerField()
    active:bool = models.BooleanField(default=True)
    def total_price(self) -> int:
        return self.product.price * self.count
    
    @property
    def ball(self) -> int:
        return self.product.diller_ball * self.count



class OrderGiftDiller(models.Model):
    user:Diller = models.ForeignKey(Diller, on_delete=models.SET_NULL,null=True)
    gift: Gifts = models.ForeignKey(Gifts, on_delete=models.SET_NULL,null=True)
    date: datetime = models.DateTimeField(auto_now_add=True)
    status:int = models.IntegerField(choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(3,"Rad etilgan")),default=0)