from django.db import models

# Create your models here.


class Diller(models.Model):
    chat_id = models.IntegerField()
<<<<<<< HEAD
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    
=======
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
>>>>>>> fb73c73a05f2059e2176e259149e91b5d4d60aaa
