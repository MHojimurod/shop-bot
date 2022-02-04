from django.core.management.base import BaseCommand



from diller.management.commands.diller import run as run_diller
from seller.management.commands.seller import run as run_seller
# import settings from django


class Command(BaseCommand):
    def handle(self, *args, **options):
        x= run_diller()
        y= run_seller()
        x.start()
        print("Diller started")
        y.start()
        print("seller started")
        x.join()
        print('x joined')
        y.join()
        print('y joined')

