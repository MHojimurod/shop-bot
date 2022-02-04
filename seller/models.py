
from django.db import models

from admin_panel.models import District, Gifts, Regions, Text

# Create your models here.
class Seller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    balls = models.IntegerField(default=0)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    shop = models.CharField(max_length=300,null=True,blank=True)
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""
    
    def get_gift(self, gift):
        return OrderGiftSeller.objects.create(user=self, gift=gift)




class OrderGiftSeller(models.Model):
    user = models.ForeignKey(Seller, on_delete=models.CASCADE)
    gift = models.ForeignKey("admin_panel.Gifts", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Cvitation(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    serial = models.CharField(max_length=100)
    img = models.ImageField(upload_to='cvitations/')
    date = models.DateTimeField(auto_now_add=True)