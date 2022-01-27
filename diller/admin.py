from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Diller)
admin.site.register(Busket)
admin.site.register(Busket_item)