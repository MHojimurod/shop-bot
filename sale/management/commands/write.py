from django.core.management.base import BaseCommand
import pandas as pd
from sale.models import SaleSeller
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        sellers = SaleSeller.objects.all()
        count = 0
        for i in sellers:
            text = "Bot yangilandi, qayta ishga tushirish uchun /start buyrug'ini yuboring"
            try:
        
                res = requests.get(f"https://api.telegram.org/bot6525921476:AAHn9ocU5-ik7TMuFScvpAw6BAlJwrpywkI/sendMessage?text={text}&chat_id={i.chat_id}")
                print(res.json()['ok'])

            except:
                print("not send message")
            
            count+=1
            if count == 20:
                time.sleep(1)
        print("end")