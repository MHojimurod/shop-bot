from django.db import models

# Create your models here.
class Text(models.Model):
    name = models.CharField(max_length=100)
    uz_data = models.TextField()
    ru_data = models.TextField()