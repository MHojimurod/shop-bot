from telegram import *
from telegram.ext import *
from diller.models import Diller

def get_user(update:Update) -> tuple[User,Diller]:
    user = update.message.from_user if update.message else update.callback_query.from_user
    return user, Diller.objects.filter(chat_id=user.id).first()



def is_odd(a):
    return bool(a - ((a >> 1) << 1))






def distribute(items: list, number:int) -> list:
    res:list = []
    i:int = 0
    for item in items:
        if items[i:i + number] == []:
            return res
        res.append(items[i:i + number])
        i += number
    return res


def delete_tmp_message(func:callable) -> callable:
    def wrapper(self, update:Update, context:CallbackContext):
        if 'tmp_message' in context.user_data:
            context.user_data['tmp_message'].delete()
        update.message.delete() if update.message else update.callback_query.message.delete()
        return func(self, update, context)
    return wrapper