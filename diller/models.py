from django.db import models
from admin_panel.models import *


class Diller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=0, choices=(
        (0, "Kutinmoqda"),
        (1, "Qabul qilingan"),
        (2, "Rad etilgan"),
    ))
    balls = models.IntegerField(default=2)

    def get_gift(self, gift):
        return OrderGiftDiller.objects.create(user=self, gift=gift)

    
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    @property
    def busket(self):
        b = Busket.objects.filter(diller=self, active=True, is_ordered=False).first()
        return b if b is not None else Busket.objects.create(diller=self)
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""

    def products(self):
        buskets = Busket.objects.filter(diller=self, active=True, is_ordered=True, is_purchased=True)
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
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=0,choices=((0,"Kutinmoqda"),(1,"Qabul qilingan"),(2,"Yuborilgan"),(3,"Rad etilgan")))

    payment_type = models.IntegerField(choices=((0, "Naqd"), (1, "Nasiya")), null=True, blank=True)

    is_ordered = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    def total_price(self):
        return sum([item.total_price for item in self.items])

    def add_product(self, product:Product, count:int):
        item = self.item(product)
        if item:
            item.count = count
            item.save()
        else:
            item = Busket_item.objects.create(busket=self, product=product, count=count)
        return item

    @property
    def items(self):
        return Busket_item.objects.filter(busket=self)
    
    def item(self, product:Product):
        return Busket_item.objects.filter(busket=self, product=product).first()

    def order(self, payment_type:int):
        self.payment_type = payment_type
        self.is_ordered = True
        self.save()
    
    def purchase(self):
        self.is_purchased = True
        balls = 0
        for busket_item in self.items:
            balls += busket_item.diller_ball
        self.save()
        return balls
    

    
    
class Busket_item(models.Model):
    busket = models.ForeignKey(Busket, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
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