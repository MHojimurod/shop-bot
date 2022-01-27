from django.contrib import admin

# Register your models here.
from .models import Text, Regions, District, Category, Product

admin.site.register(Text)
admin.site.register(Regions)
admin.site.register(District)
admin.site.register(Category)
admin.site.register(Product)
