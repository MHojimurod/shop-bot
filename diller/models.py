from django.db import models
from admin_panel.models import Text
# Create your models here.
from admin_panel.models import *

class  Diller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=0, choices=(
        (0, "Kutinmoqda"),
        (1, "Qabul qilingan"),
        (2, "Rad etilgan"),
    ))

    
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    @property
    def busket(self):
        b = Busket.objects.filter(diller=self, active=True).first()
        return b if b is not None else Busket.objects.create(diller=self)
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""


class Busket(models.Model):
    diller = models.ForeignKey(Diller, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def add_product(self, product:Product, count:int):
        item = Busket_item.objects.create(busket=self, product=product, count=count)
        return item
    @property
    def items(self):
        return Busket_item.objects.filter(busket=self)
    
    def item(self, product:Product):
        return Busket_item.objects.filter(busket=self, product=product).first()
    
class Busket_item(models.Model):
    busket = models.ForeignKey(Busket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    active = models.BooleanField(default=True)