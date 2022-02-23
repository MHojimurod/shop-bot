
from django.db import models

from admin_panel.models import District, Gifts, Regions, Text

# Create your models here.
class Seller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    balls = models.IntegerField(default=0)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    shop = models.CharField(max_length=300,null=True,blank=True)
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    shop_location = models.JSONField(default=dict)
    shop_passport_photo = models.ImageField(upload_to='shop_passport_photo', null=True, blank=True)
    passport_photo = models.ImageField(upload_to='passport_photo', null=True, blank=True)
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""
    
    def get_gift(self, gift):
        return OrderGiftSeller.objects.create(user=self, gift=gift)




class OrderGiftSeller(models.Model):
    user = models.ForeignKey(Seller, on_delete=models.CASCADE)
    gift = models.ForeignKey("admin_panel.Gifts", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(3,"Rad etilgan")),default=0)


class Cvitation(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    serial = models.CharField(max_length=100)
    img = models.ImageField(upload_to='cvitations/')
    date = models.DateTimeField(auto_now_add=True)