from telegram import *
from myapp.models import Saller

def get_user(self,update:Update) -> tuple:
    user = update.message.from_user if update.message else update.callback_query.from_user
    return user, Saller.objects.filter(chat_id=user.id).first()