import threading
from django.core.management.base import BaseCommand
from flask import Flask, request
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackContext, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, User
from admin_panel.models import BaseProduct, District, Promotion, Promotion_Order, Regions, Text, i18n
from diller.management.commands.decorators import delete_tmp_message, distribute, get_user

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
    MENU,
    SELECT_NEW_LANGUAGE
)

from diller.models import Busket, Diller
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
                CallbackQueryHandler(self.get_promotion,
                                     pattern="^get_promotion"),
                CommandHandler('language', self.change_language),
            ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)],
                NAME: [MessageHandler(Filters.text & not_start, self.name)],
                NUMBER: [MessageHandler(Filters.contact & not_start, self.number), MessageHandler(Filters.all & not_start, self.invalid_number)],
                REGION: [MessageHandler(Filters.text & not_start, self.region), MessageHandler(Filters.all & not_start, self.incorrect_region)],
                DISTRICT: [MessageHandler(Filters.text & not_start, self.district), MessageHandler(Filters.all & not_start, self.incorrect_district)],
                MENU: [
                    MessageHandler(Filters.regex(
                        "^(Sotib olish|Купить)"), self.buy),
                    MessageHandler(Filters.regex(
                        "^(Sotib olingan|Купленные)"), self.purchased),
                    MessageHandler(Filters.regex(
                        "^(Mening ballarim|Мои баллы)"), self.my_balls),
                    CommandHandler('language', self.change_language),
                ],
                SELECT_CATEGORY: [CallbackQueryHandler(self.buy, pattern="^category_pagination"), CallbackQueryHandler(self.start, pattern="^cancel_pagination"), CallbackQueryHandler(self.select_category, pattern="^select_category"), CallbackQueryHandler(self.cart, pattern="^cart")],

                SELECT_PRODUCT: [CallbackQueryHandler(self.select_category, pattern="^product_pagination"), CallbackQueryHandler(self.buy, pattern="^cancel_pagination"), CallbackQueryHandler(self.select_category, pattern="^select_product")],
                SELECT_PRODUCT_COUNT: [CallbackQueryHandler(self.plus_minus_count, pattern="^(product_count:minus|product_count:plus)"), CallbackQueryHandler(self.product_count, pattern="^product_count"), CallbackQueryHandler(self.clear_product_count, pattern="^clear_product_count"), CallbackQueryHandler(self.start, pattern="^cancel_count"), CallbackQueryHandler(self.add_to_cart, pattern="^add_to_cart"), CallbackQueryHandler(self.buy, pattern="^back")],
                CART: [CallbackQueryHandler(self.busket_item_count, pattern="^busket_item_count"),
                       CallbackQueryHandler(self.busket_item_remove, pattern="^remove_busket_item"), CallbackQueryHandler(self.buy, pattern="^continue"), CallbackQueryHandler(self.order, pattern="^order"), CallbackQueryHandler(self.buy, pattern="^back")],
                PURCHASED: [CallbackQueryHandler(self.purchased, pattern="product_pagination"), CallbackQueryHandler(self.start, pattern="^back")],
                PAYMENT_TYPE: [CallbackQueryHandler(self.payment_type, pattern="^payment_type"), CallbackQueryHandler(self.start, pattern="^back")],
                BALL: [CallbackQueryHandler(self.my_balls, pattern="^gift_pagination"), CallbackQueryHandler(self.select_gift, pattern="^select_gift"), CallbackQueryHandler(self.selct_gift_sure, pattern="^sure_select_gift"), CallbackQueryHandler(self.start, pattern="^back")],
                PROMOTION_COUNT: [CallbackQueryHandler(self.get_promotion, pattern="^get_promotion"), CallbackQueryHandler(self.get_promotion, pattern="^promotion_count"), CallbackQueryHandler(self.buy_promotion, pattern="^buy_promotion")],
                SELECT_NEW_LANGUAGE: [MessageHandler(
                    Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.new_language)]

            },
            fallbacks=[
                CommandHandler('start', self.start),
                CallbackQueryHandler(self.get_promotion,pattern="^get_promotion")
            ]
        )
        self.dispatcher.add_handler(self.conversation)
        self.dispatcher.add_handler(CallbackQueryHandler(
            self.order_accept, pattern="^order_accepted"))

        self.start_polling()
        print('polling')
        server = Flask(__name__)
        print('x')

        server.route('/diller_status',
                     methods=['POST', 'GET'])(self.user_state_update)
        server.route('/send_req', methods=['POST', 'GET'])(self.promotion)
        server.route("/update_status",
                     methods=["POST", 'GET'])(self.update_status_order)
        server.route("/update_status_prompt",
                     methods=["POST", 'GET'])(self.update_status_prompt)
        server.route('/sale', methods=['POST', 'GET']
                     )(self.saled_asdasdasdasdas)

        server.run("127.0.0.1", port=6002)

    def update_status_order(self):
        data = request.get_json()
        if data:
            data = data['data']
            diller = data['diller']
            status = data['status']
            busket = data['busket']
            diller: Diller = Diller.objects.filter(id=diller).first()
            if diller:
                busket: Busket = Busket.objects.filter(id=busket).first()
                if busket:

                    if status == 1:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_accepted'))
                        # diller.balls += busket.balls
                        diller.save()
                    elif status == 2:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_delivered'))
                    elif status == 3:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_denied'))
        return "x"

    def update_status_prompt(self):
        data = request.get_json()
        if data:
            data = data['data']
            diller = data['diller']
            status = data['status']
            ball = data['ball']
            diller: Diller = Diller.objects.filter(id=diller).first()
            if diller:
                try:
                    if status == 1:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_accepted'))
                        # diller.balls += ball
                        diller.save()
                    elif status == 2:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_delivered'))
                    elif status == 3:
                        self.bot.send_message(
                            chat_id=diller.chat_id, text=diller.text('order_denied'))
                except:
                    pass
        return "x"

    def user_state_update(self):
        data = request.get_json()
        if data:
            data = data['data']
            diller = Diller.objects.filter(id=data['id'])
            if diller.exists():
                diller: Diller = diller.first()
                self.bot.send_message(chat_id=diller.chat_id, text=diller.text(
                    "accept_message" if data['status'] == 1 else "reject_message",))
            else:
                pass
        return "x"

    def saled_asdasdasdasdas(self):
        data = request.get_json()
        if data:
            data = data['data']
            product = BaseProduct.objects.filter(
                serial_number=data['serial_number'])
            product = product.first()
            self.bot.send_message(
                product.diller.chat_id, f"Sizning mahsulotingiz sotildi!\nMahsulot: {product.product.name_uz if product.diller.language == 0 else product.product.name_ru}\nSeria raqami: {data['serial_number']}\nSotuvchi: {data['name']} (@{data['username']})\nTelefon: {data['number']}\nViloyat: {data['region']}")
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
                                    InlineKeyboardButton(diller.text(
                                        'i_bought'), callback_data=f"get_promotion:{pr.id}"),
                                ]
                            ]
                        ))
                    except:
                        pass
                    ids.append(diller.id)
        return str(ids)

    def get_promotion(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(':')
        if data[0] == 'get_promotion':
            product:Promotion = Promotion.objects.filter(
                id=int(update.callback_query.data.split(':')[1]))
            if product.exists():
                product = product.first()
                if product.available > 0:
                    context.user_data['promotion_count'] = 1
                    context.user_data['promotion_product'] = product
                    update.callback_query.message.edit_text(
                        product.description_uz if db_user.language == 1 else product.description_ru, reply_markup=promotion_keyboard(db_user, context))
                else:
                    update.callback_query.message.edit_text(
                        db_user.text("prompt_end"))
            else:
                update.callback_query.message.edit_text(
                    db_user.text("prompt_end"))
        elif data[0] == "promotion_count":
            count = int(data[1])
            if count <= context.user_data['promotion_product'].count:
                context.user_data['promotion_count'] = count
                update.callback_query.message.edit_text(text=db_user.text(
                    "promotion_count_message") + str(count), reply_markup=promotion_keyboard(db_user, context))
            else:
                update.callback_query.answer(text=db_user.text(
                    "promotion_count_error"), show_alert=True)

        return PROMOTION_COUNT

    def buy_promotion(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if context.user_data['promotion_count'] > 0:
            count = context.user_data['promotion_count']
            product = context.user_data['promotion_product']
            context.user_data['promotion_count'] = 0
            context.user_data['promotion_product'] = None
            if count <= product.available:
                product.bought_count += count
                product.save()
                order = Promotion_Order.objects.create(
                    user=db_user, promotion=product, count=count)
                update.callback_query.message.edit_text(text=db_user.text(
                    "order_accepted"), reply_markup=InlineKeyboardMarkup([]))
                return self.start(update, context, False)
            else:
                update.callback_query.answer(
                    text=db_user.text("prompt_end"), show_alert=True)
                return self.start(update, context, False)

    @delete_tmp_message
    def change_language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(text=Text.objects.filter(name='start').first().uz_data, reply_markup=ReplyKeyboardMarkup(
            [
                ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
            ],
            resize_keyboard=True
        ), parse_mode="HTML")
        return SELECT_NEW_LANGUAGE

    @delete_tmp_message
    def new_language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        db_user.language = lang = 0 if update.message.text.startswith(
            "🇺🇿") else (1 if update.message.text.startswith("🇷🇺") else None)
        db_user.save()
        if lang is not None:
            return self.start(update, context, False)
        else:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message("language_not_found", reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ], resize_keyboard=True
            ), parse_mode="HTML")
            return SELECT_NEW_LANGUAGE

    @delete_tmp_message
    def invalid_number(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['tmp_message'] = update.message.reply_text(i18n("invalid_number", context.user_data['register']['language']), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(i18n("send_number", context.user_data['register']['language']),
                                   request_contact=True),
                ]
            ], resize_keyboard=True
        ))
        return NUMBER

    @delete_tmp_message
    def incorrect_region(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['tmp_message'] = update.message.reply_text(i18n("region_not_found", context.user_data['register']['language']), reply_markup=ReplyKeyboardMarkup(
            distribute([
                region.name(context.user_data['register']['language']) for region in Regions.objects.all()
            ], 2), resize_keyboard=True
        ))
        return REGION

    @delete_tmp_message
    def incorrect_district(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['tmp_message'] = update.message.reply_text(i18n("district_not_found", context.user_data['register']['language']), reply_markup=ReplyKeyboardMarkup(
            distribute([
                region.name(context.user_data['register']['language']) for region in District.objects.all()
            ], 2), resize_keyboard=True
        ))
        return REGION


work = Bot(TOKEN)


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
