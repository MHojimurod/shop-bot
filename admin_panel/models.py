from datetime import datetime
from django.db import models

# from seller.models import Seller


# from seller.models import Seller

# from diller.models import Diller

# Create your models here.
class Text(models.Model):
    id:int
    name:str = models.CharField(max_length=100)
    uz_data:str = models.TextField()
    ru_data:str = models.TextField()

    def __str__(self):
        return self.name


def i18n(name:str, lang:int=1):

    text = Text.objects.filter(name=name)
    return (text.first().uz_data if lang == 0 else text.first().ru_data) if text.exists() else ""



class Regions(models.Model):
    id:int
    uz_data: str = models.TextField()
    ru_data: str = models.TextField()
    def name(self, lang:int):
        return self.uz_data if lang == 0 else self.ru_data

    def __str__(self):
        return self.ru_data
    @property
    def seller_count(self):
        data = "Seller".objects.filter(status=1,region=self)
        active = "Seller".objects.filter(status=1,balls__gt=0).count()
        balls = 0
        for i in data:
            balls+= i.balls
        return data.count(), balls, active   
class District(models.Model):
    id:int
    region: Regions = models.ForeignKey(Regions, on_delete=models.CASCADE)
    uz_data: str = models.TextField()
    ru_data: str = models.TextField()

    def name(self, lang:int):
        return self.uz_data if lang == 0 else self.ru_data

    def __str__(self):
        return self.ru_data

class Category(models.Model):
    id:int
    name_uz: str = models.CharField(max_length=100)
    name_ru: str = models.CharField(max_length=100)
    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru


class Product(models.Model):
    id:int
    category:Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_uz: str = models.CharField(max_length=100)
    name_ru: str = models.CharField(max_length=100)
    diller_ball: int = models.IntegerField()
    diller_nasiya_ball:int = models.IntegerField()
    seller_ball:int = models.IntegerField()
    price: float = models.IntegerField()
    image = models.ImageField(upload_to='products')
    code = models.CharField(max_length=10,null=True,blank=True)
    last_code = models.IntegerField(default=0)


    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru

    def description(self, lang:int):
        return self.description_uz if lang == 0 else self.description_ru

    def __str__(self):
        return self.name_uz

class Gifts(models.Model):
    id:int
    gift_type:int = models.IntegerField(choices=((0, "Diller"), (1, "Sotuvchi")))
    name_uz:int = models.CharField(max_length=100)
    name_ru:int = models.CharField(max_length=100)
    ball:int = models.IntegerField()
    amount:int = models.IntegerField()
    image = models.ImageField(upload_to='gifts')

    def name(self, lang:int):
        return self.name_uz if lang == 0 else self.name_ru

    def take(self, user):
        self.amount-=1
        self.save()
        user.balls = user.balls-self.ball
        user.save()
        return user.get_gift(gift=self)



class   BaseProduct(models.Model):
    id:int
    diller = models.ForeignKey("diller.Diller", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey("seller.Seller", on_delete=models.SET_NULL, null=True)
    product:Product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    serial_number:str = models.CharField(max_length=200)
    is_active:bool = models.BooleanField(default=False)
    date:datetime = models.DateTimeField(auto_now_add=True)

    
    def sale(self):
        self.is_active = True
        self.save()


class Promotion(models.Model):
    id:int
    product: Product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    price:int = models.FloatField()
    ball:int = models.IntegerField()
    active:bool = models.BooleanField(default=False)
    description_uz:str = models.TextField()
    description_ru:str = models.TextField()
    count:int = models.IntegerField()
    bought_count:int = models.IntegerField(default=0,null=True,blank=True)
    @property
    def available(self) -> int:
        return self.count - self.bought_count



class Promotion_Order(models.Model):
    id:int
    user  = models.ForeignKey("diller.Diller", on_delete=models.CASCADE)
    promotion:Promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    count:int = models.IntegerField(default=1)  
    date:datetime = models.DateTimeField(auto_now_add=True)
    status:int = models.IntegerField(default=0,choices=((0,"Kutilmoqda"),(1,"Qabul qilingan"),(2,"Yuborilgan"),(3,"Rad etilgan")))
