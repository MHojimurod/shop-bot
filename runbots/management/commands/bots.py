import threading
from django.core.management.base import BaseCommand



import os


def run_diller():
    os.system("python manage.py diller")
def run_seller():
    os.system("python manage.py seller")
class Command(BaseCommand):
    def handle(self, *args, **options):
        threading.Thread(target=run_diller).start()
        threading.Thread(target=run_seller).start()
        print("Diller is running...")