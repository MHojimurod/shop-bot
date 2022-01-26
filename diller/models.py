from django.db import models

# Create your models here.


class Diller(models.Model):
    chat_id = models.IntegerField()
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))