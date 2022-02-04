from diller.management.commands.diller import Bot as Diller, TOKEN as Diller_Token
from seller.management.commands.seller import Bot as Seller, TOKEN as Seller_Token

import threading


diller = threading.Thread(target=Diller.__init__, args=(Diller_Token,))
seller = threading.Thread(target=Seller.__init__, args=(Seller_Token,))



diller.start()
seller.start()
diller.join()
seller.join()