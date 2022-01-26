from django.db import models

# Create your models here.
class Text(models.Model):
    name = models.CharField(max_length=100)
    uz_data = models.TextField()
    ru_data = models.TextField()

    def __str__(self) -> str:
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