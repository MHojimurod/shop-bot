from telegram import *
from myapp.models import Seller

def get_user(update:Update) -> tuple:
    user = update.message.from_user if update.message else update.callback_query.from_user
    return user, Seller.objects.filter(chat_id=user.id).first()