from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackContext, CallbackQueryHandler)
from telegram import User

from diller.stages.busket import BusketHandlers
from .constant import (
    BALL,
    CART,
    PAYMENT_TYPE,
    PURCHASED,
    SELECT_CATEGORY,
    SELECT_PRODUCT,
    SELECT_PRODUCT_COUNT,
    TOKEN,
    LANGUAGE,
    NAME,
    NUMBER,
    REGION,
    DISTRICT,
    MENU
)

from diller.models import Diller
from diller.stages import Register, Menu, Buy


user: User
db_user: Diller


class Bot(Updater, Register, Menu, Buy, BusketHandlers):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        not_start = ~Filters.regex("^(\/start)")

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start),
                MessageHandler(Filters.regex(
                        "^(Sotib olish|Купить)"), self.buy),
                    MessageHandler(Filters.regex(
                        "^(Sotib olingan|Купленные)"), self.purchased),
                    MessageHandler(Filters.regex(
                        "^(Mening ballarim|Мои баллы)"), self.my_balls)
            ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)],
                NAME: [MessageHandler(Filters.text & not_start, self.name)],
                NUMBER: [MessageHandler(Filters.contact & not_start, self.number)],
                REGION: [MessageHandler(Filters.text & not_start, self.region)],
                DISTRICT: [MessageHandler(Filters.text & not_start, self.district)],
                MENU: [
                    MessageHandler(Filters.regex(
                        "^(Sotib olish|Купить)"), self.buy),
                    MessageHandler(Filters.regex(
                        "^(Sotib olingan|Купленные)"), self.purchased),
                    MessageHandler(Filters.regex(
                        "^(Mening ballarim|Мои баллы)"), self.my_balls)
                ],
                SELECT_CATEGORY: [CallbackQueryHandler(self.buy, pattern="^category_pagination"), CallbackQueryHandler(self.start, pattern="^cancel_pagination"), CallbackQueryHandler(self.select_category, pattern="^select_category"), CallbackQueryHandler(self.cart, pattern="^cart")],
                
                SELECT_PRODUCT: [ CallbackQueryHandler(self.select_category, pattern="^product_pagination"), CallbackQueryHandler(self.buy, pattern="^cancel_pagination"), CallbackQueryHandler(self.select_category, pattern="^select_product")],
                SELECT_PRODUCT_COUNT: [CallbackQueryHandler(self.product_count, pattern="^product_count"), CallbackQueryHandler(self.start, pattern="^cancel_count"), CallbackQueryHandler(self.add_to_cart, pattern="^add_to_cart"), CallbackQueryHandler(self.buy, pattern="^back")],
                CART: [CallbackQueryHandler(self.busket_item_count, pattern="^busket_item_count"),
                CallbackQueryHandler(self.busket_item_remove, pattern="^remove_busket_item"), CallbackQueryHandler(self.buy, pattern="^continue"), CallbackQueryHandler(self.order, pattern="^order"), CallbackQueryHandler(self.buy, pattern="^back")],
                PURCHASED: [ CallbackQueryHandler(self.purchased, pattern="product_pagination"), CallbackQueryHandler(self.start, pattern="^back")],
                PAYMENT_TYPE: [CallbackQueryHandler(self.payment_type, pattern="^payment_type"), CallbackQueryHandler(self.start, pattern="^back")],
                BALL: [CallbackQueryHandler(self.my_balls, pattern="^gift_pagination"), CallbackQueryHandler(self.select_gift, pattern="^select_gift"), CallbackQueryHandler(self.selct_gift_sure, pattern="^sure_select_gift"), CallbackQueryHandler(self.start, pattern="^back")],
            },
            fallbacks=[
                CommandHandler('start', self.start)
            ]
        )
        self.dispatcher.add_handler(self.conversation)
        self.dispatcher.add_handler(CallbackQueryHandler(self.order_accept, pattern="^order_accepted"))

        self.start_polling()
        print('polling')
        self.idle()


x = Bot(TOKEN)