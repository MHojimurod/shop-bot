from http.client import PAYMENT_REQUIRED
from telegram import *
from telegram.ext import *
from diller.management.commands.constant import MENU, PAYMENT_TYPE
from diller.management.commands.decorators import distribute, get_user
from diller.models import Busket, Busket_item, Diller
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
            if len(db_user.busket.items) > 0:
                update.callback_query.message.edit_text(**busket_keyboard(db_user, context), parse_mode="HTML")
            else:
                update.callback_query.answer(db_user.text("empty_busket"), show_alert=True)
                update.callback_query.message.delete()
                return self.start(update, context)
    
    def order(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if len(db_user.busket.items) > 0:
            # db_user.busket.order()
            # update.callback_query.message.edit_text("Sizning buyurtmalaringiz qabul qilindi!", parse_mode="HTML")
            # return self.start(update, context)
            update.callback_query.message.edit_text(text=db_user.text("pay_type"), parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(db_user.text("cash"), callback_data="payment_type:0"), InlineKeyboardButton(db_user.text("loan"), callback_data="payment_type:1")]]))
            return PAYMENT_TYPE
    
    def payment_type(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        user_busket = db_user.busket
        user_busket.order(int(data[1]))
        update.callback_query.message.edit_text(**wait_accept_keyboard(db_user, user_busket), parse_mode="HTML")
        context.user_data['tmp_message'] = user.send_message("menu", reply_markup=ReplyKeyboardMarkup(
                    distribute([db_user.text("buy"), db_user.text("taken"), db_user.text('my_balls')], 2), resize_keyboard=True
                ), parse_mode="HTML")
        return MENU
    
    def order_accept(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        busket = Busket.objects.filter(id=int(data[1]))
        if busket.exists():
            if busket.first().status == 2:
                text = {
                    # 0:"Sizning hisobingizga %d ball qo'shildi!",
                    0:"Haridingiz uchun raxmat!",
                    1:"Спасибо за покупку!"
                }
                busket.update(status=4)
                update.callback_query.message.edit_text(text[db_user.language], parse_mode="HTML")
            else:
                update.callback_query.answer(db_user.text("order_not_accepted_yet"), show_alert=True)