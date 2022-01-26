from telegram import *
from diller.models import Diller

def get_user(update:Update) -> tuple[User,Diller]:
    user = update.message.from_user if update.message else update.callback_query.from_user
    return user, Diller.objects.filter(chat_id=user.id).first()



def is_odd(a):
    return bool(a - ((a >> 1) << 1))






def distribute(items, number) -> list:
    res = []
    start = 0
    end = number
    for item in items:
        if items[start:end] == []:
            return res
        res.append(items[start:end])
        start += number
        end += number
    return res