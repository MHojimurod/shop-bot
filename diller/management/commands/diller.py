from click import BaseCommand
from flask import Flask, request
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackContext, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from admin_panel.models import Promotion, Promotion_Order, i18n
from diller.management.commands.decorators import get_user

from diller.stages.busket import BusketHandlers
from diller.utils import promotion_keyboard
from .constant import (
    BALL,
    CART,
    PAYMENT_TYPE,
    PROMOTION_COUNT,
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
                        "^(Mening ballarim|Мои баллы)"), self.my_balls),
                    CallbackQueryHandler(self.get_promotion, pattern="^get_promotion")
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
                PROMOTION_COUNT: [CallbackQueryHandler(self.get_promotion, pattern="^get_promotion"), CallbackQueryHandler(self.get_promotion, pattern="^promotion_count"), CallbackQueryHandler(self.buy_promotion, pattern="^buy_promotion")],
            },
            fallbacks=[
                CommandHandler('start', self.start),
                CallbackQueryHandler(self.get_promotion, pattern="^get_promotion")
            ]
        )
        self.dispatcher.add_handler(self.conversation)
        self.dispatcher.add_handler(CallbackQueryHandler(self.order_accept, pattern="^order_accepted"))

        self.start_polling()
        print('polling')
        server = Flask(__name__)
        print('x')

        server.route('/diller_status', methods=['POST', 'GET'])(self.user_state_update)
        server.route('/send_req', methods=['POST', 'GET'])(self.promotion)

        server.run("127.0.0.1",port=6002)

    def user_state_update(self):
        data = request.get_json()
        if data:
            data = data['data']
            diller = Diller.objects.filter(id=data['id'])
            if diller.exists():
                diller = diller.first()
                self.bot.send_message(chat_id=diller.chat_id, text = i18n("accept_message" if data['status'] == 1 else "reject_message"))
            else:
                pass
        return "x"

    def promotion(self):
        data = request.get_json()
        if data:
            ids = []
            data = data['data']
            pr = Promotion.objects.filter(id=data['product'])
            if pr.exists():
                pr = pr.first()
                for diller in Diller.objects.filter(status=1):
                    try:
                        self.bot.send_message(chat_id=diller.chat_id, text=pr.description_uz if diller.language == 0 else pr.description_ru, reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(diller.text('i_bought'), callback_data=f"get_promotion:{pr.id}"),
                            ]
                        ]
                    ))
                    except:
                        pass
                    ids.append(diller.id)
        return str(ids)
    
    def get_promotion(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(':')
        if data[0] == 'get_promotion':
            product = Promotion.objects.filter(id=int(update.callback_query.data.split(':')[1]))
            if product.exists():
                product = product.first()
                if product.available > 0:
                    context.user_data['promotion_count'] = 1
                    context.user_data['promotion_product'] = product
                    update.callback_query.message.edit_text("xxxx", reply_markup=promotion_keyboard(db_user, context))
                else:
                    update.callback_query.message.edit_text("Kechirasiz aksiya tugadi!")
            else:
                update.callback_query.message.edit_text("Kechirasiz aksiya tugadi!")
        elif data[0] == "promotion_count":
            count = int(data[1])
            if count <= context.user_data['promotion_product'].count:
                context.user_data['promotion_count'] = count
                update.callback_query.message.edit_text(text=i18n("promotion_count_message") + str(count), reply_markup=promotion_keyboard(db_user,context))
            else:
                update.callback_query.answer(text=i18n("promotion_count_error") +  "x", show_alert=True)

        return PROMOTION_COUNT

    def buy_promotion(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        print('x')
        if context.user_data['promotion_count'] > 0:
            count = context.user_data['promotion_count']
            product = context.user_data['promotion_product']
            context.user_data['promotion_count'] = 0
            context.user_data['promotion_product'] = None
            if count <= product.available:
                product.bought_count += count
                product.save()
                order = Promotion_Order.objects.create(user=db_user, promotion=product, count=count)
                update.callback_query.message.edit_text('Sizning buyurtmangiz qabul qilindi', reply_markup=InlineKeyboardMarkup([]))
                return self.start(update, context, False)
            else:
                update.callback_query.answer("Kechirasiz aksiyalar soni tugadi!", show_alert=True)
                return self.start(update, context, False)
            
x = Bot(TOKEN)



class Command(BaseCommand):
    def handle(self, *args, **options):
        print('x')












# asdfsdfsdfsdf