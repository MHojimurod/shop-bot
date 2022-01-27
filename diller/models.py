from django.db import models
from admin_panel.models import Text
# Create your models here.
from admin_panel.models import *

class  Diller(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    
    language = models.IntegerField(choices=((0, 'uz'), (1, 'ru')))
    
    def text(self, name):
        text = Text.objects.filter(name=name)
        return (text.first().uz_data if self.language == 0 else text.first().ru_data) if text.exists() else ""
