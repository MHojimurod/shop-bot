from email.message import Message
from telegram.ext import (Updater, Filters, CallbackQueryHandler, CallbackContext, ConversationHandler, CommandHandler, MessageHandler)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from admin_panel.models import BaseProduct, Gifts, i18n
from seller.management.commands.decorators import get_user


from seller.models import Seller
from seller.utils import balls_keyboard_pagination
from .constant import (
    CVI,
    CVI_PHOTO,
    CVI_SERIAL_NUMBER,
    LANGUAGE,
    SHOP,
    TOKEN,
    NUMBER,
    NAME,
    REGION,
    DISTRICT,
    MENU,
    BALL
)
from flask import Flask, request

from seller.stages import MainHandlers

user: User
db_user: Seller

class Bot(Updater, MainHandlers):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        not_start = ~Filters.regex("^(\/start)")

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.start),
            ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)],
                NAME: [MessageHandler(Filters.text & not_start, self.name)],
                NUMBER: [MessageHandler(Filters.contact & not_start, self.number)],
                REGION: [MessageHandler(Filters.text & not_start, self.region)],
                DISTRICT: [MessageHandler(Filters.text & not_start, self.district)],
                SHOP: [MessageHandler(Filters.text, self.shop)],
                MENU: [
                    MessageHandler(Filters.regex("^(Kvitansiya|Kvitansiya)"), self.cvitation),
                    MessageHandler(Filters.regex("^(Mening ballarim|Мои баллы)"), self.my_balls),
                ],
                CVI: [MessageHandler(Filters.photo, self.cvi_photo)],
                CVI_PHOTO: [MessageHandler(Filters.photo, self.cvi_photo)],
                CVI_SERIAL_NUMBER: [MessageHandler(Filters.text, self.cvi_serial_number)],
                BALL: [CallbackQueryHandler(self.my_balls, pattern="^gift_pagination"), CallbackQueryHandler(self.select_gift, pattern="^select_gift"), CallbackQueryHandler(self.selct_gift_sure, pattern="^sure_select_gift"), CallbackQueryHandler(self.start, pattern="^back")],
            },
            fallbacks=[CommandHandler("start", self.start)],
        )
        self.dispatcher.add_handler(self.conversation)
        self.start_polling()
        print('polling')
        print('x')
        self.idle()
        

    def cvitation(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        user.send_message(i18n("send_cvitation"))
        return CVI_PHOTO
    
    def cvi_photo(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        user.send_message(i18n("send_cvi_serial_number"))
        return CVI_SERIAL_NUMBER
    
    def cvi_serial_number(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        product = BaseProduct.objects.filter(serial_number=update.message.text)
        if product.exists():
            product:BaseProduct = product.first()
            user.send_message("Sizning kvitansiyangiz qabul qilindi!\nBiz dillerga sotilgani haqida habaar beramiz!")
            product.sale(db_user)
            context.bot.send_message(product.diller.chat_id, f"Sizning mahsulotingiz sotildi!\nMahsulot: {product.product.name(db_user.language)}\nSeria raqami: {product.serial_number}\nSotuvchi: {db_user.name} (@{user.username})")
            return self.start(update, context,False)
        else:
            user.send_message("Kechirasiz seria raqamni topilmadi!")
        return CVI_PHOTO
    
    def my_balls(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.message:
            context.user_data['tmp_message'] = user.send_message(**balls_keyboard_pagination(db_user, 1), parse_mode="HTML",)
            return BALL
        else:
            data = update.callback_query.data.split(":")
            if data[0] == "gift_pagination":
                update.callback_query.message.edit_text(**balls_keyboard_pagination(db_user, int(data[1])), parse_mode="HTML")
                return BALL
            else:
                update.callback_query.message.edit_text(**balls_keyboard_pagination(db_user, 1), parse_mode="HTML")
                return BALL
    
    def select_gift(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        if data[0] == "select_gift":
            gift = Gifts.objects.filter(id=int(data[1]))
            if gift.exists():
                if gift.first().ball <= db_user.balls:
                    context.user_data['current_gift'] = gift.first()
                    update.callback_query.message.edit_text(i18n("are_you_sure_get_gift", db_user.language),    parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(i18n("yes", db_user.language), callback_data="sure_select_gift:yes"),
                            InlineKeyboardButton(i18n("no", db_user.language), callback_data="sure_select_gift:no")
                        ]
                    ]))
                    return BALL
                else:
                    update.callback_query.answer("Sizning balansingizda kifayot emas")
    def selct_gift_sure(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        data = update.callback_query.data.split(":")
        if data[0] == "sure_select_gift":
            if data[1] == "yes":
                context.user_data['current_gift'].take(db_user)
                update.callback_query.message.edit_text("Sizning so'rovingiz qabul qilindi!\nTez orada o'zimiz tilifon qivoramiz!")
                return self.start(update, context, False)
            else:
                return self.my_balls(update, context)

x = Bot(TOKEN)