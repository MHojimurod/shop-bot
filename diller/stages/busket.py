from http.client import PAYMENT_REQUIRED
from telegram import *
from telegram.ext import *
from diller.management.commands.constant import PAYMENT_TYPE
from diller.management.commands.decorators import get_user
from diller.models import Busket_item, Diller
from admin_panel.models import Category, Product, i18n
from diller.utils import busket_keyboard, wait_accept_keyboard

class BusketHandlers:
    def busket_item_count(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        item = Busket_item.objects.filter(id=int(data[1]))
        if item.exists():
            item.update(count=int(data[2]))
            update.callback_query.message.edit_text(**busket_keyboard(db_user, context), parse_mode="HTML")
    
    def busket_item_remove(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        item = Busket_item.objects.filter(id=int(data[1]))
        if item.exists():
            item.delete()
            print(len(db_user.busket.items))
            if len(db_user.busket.items) > 0:
                update.callback_query.message.edit_text(**busket_keyboard(db_user, context), parse_mode="HTML")
            else:
                update.callback_query.answer("Kechirasiz bo'limda hech qanday mahsulot qolmadi!", show_alert=True)
                update.callback_query.message.delete()
                return self.start(update, context)
    
    def order(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if len(db_user.busket.items) > 0:
            # db_user.busket.order()
            # update.callback_query.message.edit_text("Sizning buyurtmalaringiz qabul qilindi!", parse_mode="HTML")
            # return self.start(update, context)
            update.callback_query.message.edit_text("Pulini naqd to'laysizmi yoki nasiyadami?", parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Naqd", callback_data="payment_type:0"), InlineKeyboardButton("Nasiya", callback_data="payment_type:1")]]))
            return PAYMENT_TYPE
    
    def payment_type(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        user_busket = db_user.busket
        user_busket.order(int(data[1]))
        update.callback_query.message.edit_text(**wait_accept_keyboard(db_user, user_busket), parse_mode="HTML")
        return self.start(update, context, False)
    
    def order_accept(self, update: Update, context: CallbackContext):
        # user, db_user = get_user(update)
        # data = update.callback_query.data.split(":")
        # user_busket = Busket_item.objects.filter(id=int(data[1]))
        # if user_busket.exists():
        #     user_busket.update(status=1)
        #     update.callback_query.message.edit_text("Sizning buyurtmaningiz qabul qilindi!", parse_mode="HTML")
        #     return self.start(update, context)
        pass