
from datetime import datetime
from hashlib import blake2b
from pyexpat import model
from tkinter import TRUE
from django.db import models

from admin_panel.models import District, Gifts, Regions, Text

# Create your models here.
class Seller(models.Model):
    id:int
    chat_id:int = models.IntegerField()
    name:str = models.CharField(max_length=100)
    number:str = models.CharField(max_length=100)
    balls:int = models.IntegerField(default=0)
    region: Regions = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district: District = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    shop:str = models.CharField(max_length=300,null=True,blank=True)
    language:int = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    shop_location: dict = models.JSONField(default=dict)
    shop_passport_photo = models.ImageField(upload_to='shop_passport_photo', null=True, blank=True)
    passport_photo = models.ImageField(upload_to='passport_photo', null=True, blank=True)
    dillers = models.ManyToManyField("diller.Diller")
    status:int = models.IntegerField(default=0, choices=(
        (0, "Kutilmoqda"),
        (1, "Qabul qilingan"),
        (2, "Rad etilgan"),
    ))
    
    def text(self, name) -> str:
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""
    
    def get_gift(self, gift) -> "OrderGiftSeller":
        return OrderGiftSeller.objects.create(user=self, gift=gift)

    def __str__(self):
        return self.name
    


class OrderGiftSeller(models.Model):
    user: Seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    gift= models.ForeignKey("admin_panel.Gifts", on_delete=models.CASCADE)
    date: datetime = models.DateTimeField(auto_now_add=True)
    status:int = models.IntegerField(choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(3,"Rad etilgan")),default=0)


class Cvitation(models.Model):
    seller: Seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    serial:str = models.CharField(max_length=100)
    img = models.ImageField(upload_to='cvitations/')
    date:datetime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0,choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(3,"Rad etilgan")))
    current_ball = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)