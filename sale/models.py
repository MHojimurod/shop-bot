from django.db import models
from seller.models import Regions

class SaleSeller(models.Model):
    chat_id = models.BigIntegerField()
    language = models.CharField(max_length=2)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    holder_name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
