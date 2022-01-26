from telegram import *
from telegram.ext import *
from myapp.models import Seller
from myapp.management.commands.buttons import *

def get_user(update:Update) -> tuple:
    user = update.message.from_user if update.message else update.callback_query.from_user
    return user, Seller.objects.filter(chat_id=user.id).first()


def register(func):
    def wrapper(self,update:Update,context:CallbackContext):
        user,db_user = get_user(update)
        info_user = context.user_data.get("user",0)
        if info_user:
            if info_user["chat_id"]:
                context.bot.send_message(text="tilni tanlang",reply_markup=lang_btn())
                return 
                

        else:
            context.user_data['user'] = {"chat_id": user.id}
    return wrapper
