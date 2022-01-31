from email.message import Message
from math import prod
from telegram.ext import (Updater, Filters, CallbackQueryHandler, CallbackContext, ConversationHandler, CommandHandler, MessageHandler)

from telegram import Update, User
from admin_panel.models import BaseProduct, i18n
from seller.management.commands.decorators import get_user


from seller.models import Seller
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
    MENU
)

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
            },
            fallbacks=[CommandHandler("start", self.start)],
        )
        self.dispatcher.add_handler(self.conversation)
        self.start_polling()
        print('polling')
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

x = Bot(TOKEN)