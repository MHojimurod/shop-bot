from django.db import models
from django.urls import include


# from seller.models import Seller

# from diller.models import Diller

# Create your models here.
class Text(models.Model):
    name = models.CharField(max_length=100)
    uz_data = models.TextField()
    ru_data = models.TextField()

    def __str__(self):
        return self.name


def i18n(name:str, lang:int=1):
    text = Text.objects.filter(name=name)
    return (text.first().uz_data if lang == 0 else text.first().ru_data) if text.exists() else ""



class Regions(models.Model):
    uz_data = models.TextField()
    ru_data = models.TextField()
    def name(self, lang:int):
        return self.uz_data if lang == 0 else self.ru_data



class District(models.Model):
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    uz_data = models.TextField()
    ru_data = models.TextField()

    def name(self, lang:int):
        return self.uz_data if lang == 0 else self.ru_data


class Category(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru














class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    diller_ball = models.IntegerField()
    diller_nasiya_ball = models.IntegerField()
    seller_ball = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products')


    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru

    def description(self, lang:int):
        return self.description_uz if lang == 0 else self.description_ru

    def __str__(self):
        return self.name_uz

class Gifts(models.Model):
    gift_type = models.IntegerField(choices=((0, "Diller"), (1, "Sotuvchi")))
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    ball = models.IntegerField()
    image = models.ImageField(upload_to='gifts')

    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru

    def take(self, user):
        return user.get_gift(gift=self)



class BaseProduct(models.Model):
    diller = models.ForeignKey("diller.Diller", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

   
    def sale(self):
        self.is_active = True
        self.save()


class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    price = models.IntegerField()
    ball = models.IntegerField()
    active = models.BooleanField(default=False)
    description_uz = models.TextField()
    description_ru = models.TextField()
    count = models.IntegerField()
    bought_count = models.IntegerField(default=0,null=True,blank=True)
    @property
    def available(self):
        return self.count - self.bought_count



class Promotion_Order(models.Model):
    user = models.ForeignKey("diller.Diller", on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)  
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0,choices=((0,"Kutinmoqda"),(1,"Qabul qilingan"),(2,"Yuborilgan"),(3,"Rad etilgan")))
