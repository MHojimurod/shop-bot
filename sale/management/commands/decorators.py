from telegram import *
from telegram.ext import *
from sale.models import SaleSeller

def get_user(update:Update):
    user = update.message.from_user if update.message else update.callback_query.from_user
    db_user, created = SaleSeller.objects.get_or_create(chat_id=user.id)
    return user, db_user



def is_odd(a):
    return bool(a - ((a >> 1) << 1))






def distribute(items: list, number:int):
    res:list = []
    i:int = 0
    for item in items:
        if items[i:i + number] == []:
            return res
        res.append(items[i:i + number])
        i += number
    return res


def delete_tmp_message(func:callable):
    def wrapper(self, update:Update, context:CallbackContext):
        if 'tmp_message' in context.user_data:
            try:
                context.user_data['tmp_message'].delete()
            except:pass
        try:
            update.message.delete() if update.message else update.callback_query.message.delete()
        except:
            pass
        return func(self, update, context)
    return wrapper