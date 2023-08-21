from django.db import models
from seller.models import Regions


class SaleSeller(models.Model):
    WAITING = 1
    CANCELED = -1
    ACCEPT = 2
    chat_id = models.BigIntegerField()
    language = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
    state = models.SmallIntegerField(default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.BigIntegerField(default=0)

    def set_language(self, language):
        self.language = language
        self.save()

    def set_name(self, name):
        self.name = name
        self.save()

    def set_phone(self, phone):
        self.phone = phone
        self.save()

    def set_region(self, region):
        self.region = region
        self.save()


class Card(models.Model):
    holder_name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
