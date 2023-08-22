from django.core.management.base import BaseCommand
import pandas as pd
from sale.models import SerialNumbers

class Command(BaseCommand):
    def handle(self, *args, **options):
        excel = open('sale/management/commands/excel.xlsx', 'rb')
        for i in range(4):
            df = pd.read_excel(excel, sheet_name=i).to_dict()
            code = df.get("code", None)
            price = df.get("price", None)
            SerialNumbers
            for key, value in code.items():
                SerialNumbers.objects.get_or_create(code=value, cashback=price[key])
                
        
        _list = [
            {
                "code":1217581,
                "cashback":5
            },
            {
                "code":1229247,
                "cashback":7
            },
            {
                "code":1835610,
                "cashback":10
            },
            {
                "code": 1440870,
                "cashback":100
            }
        ]
        for i in _list:
            SerialNumbers.objects.get_or_create(**i)