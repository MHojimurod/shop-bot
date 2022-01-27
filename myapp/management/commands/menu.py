from telegram.ext import (CallbackContext)
from telegram import (Update,ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from diller.management.commands.decorators import delete_tmp_message, distribute
from myapp.management.commands.constant import (
    MENU
)
from myapp.management.commands.decorators import get_user
from admin_panel.models import District, Regions, Text, i18n
from myapp.models import Seller


class Menu:
    @delete_tmp_message
    def buy(self, update:Update, context:CallbackContext):
        print(update.message.text)
        return MENU

    def purchased(self, update:Update, context:CallbackContext):
        print("aaa")
        print(update.message.text)
        return MENU

    def my_balls(self, update:Update, context:CallbackContext):
        print("aaa")
        print(update.message.text)
        return MENU
        

    