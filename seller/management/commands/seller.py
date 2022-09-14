from uuid import uuid4
from django import db
from flask import Flask, request
from telegram.ext import (Updater, Filters, CallbackQueryHandler, CallbackContext, ConversationHandler, CommandHandler, MessageHandler)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, User
from admin_panel.models import BaseProduct, District, Gifts, Regions, Text,  i18n
from diller.management.commands.decorators import delete_tmp_message, distribute
from seller.management.commands.decorators import get_user

import requests
from seller.models import Cvitation, Seller
from seller.utils import balls_keyboard_pagination
from .constant import (
    CVI_PHOTO,
    CVI_SERIAL_NUMBER,
    LANGUAGE,
    SELECT_NEW_LANGUAGE,
    SHOP,
    TOKEN,
    NUMBER,
    NAME,
    REGION,
    DISTRICT,
    MENU,
    BALL,
    SHOP_LOCATION,
    PASSPORT_PHOTO,
    SHOP_PASSPORT_PHOTO
)


# from seller.stages import MainHandlers

user: User = None
db_user: Seller = None




class Bot(Updater):
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN, *args, **kwargs)

        not_start = ~Filters.regex("^(\/start)")

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.start),
            ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)],
                NAME: [MessageHandler(Filters.text & not_start, self.name)],
                NUMBER: [MessageHandler(Filters.contact & not_start, self.number), MessageHandler(Filters.all & not_start, self.invalid_number)],
                REGION: [MessageHandler(Filters.text & not_start, self.region), MessageHandler(Filters.all & not_start, self.incorrect_region)],
                DISTRICT: [MessageHandler(Filters.text & not_start, self.district), MessageHandler(Filters.all & not_start, self.incorrect_district)],
                SHOP_LOCATION: [MessageHandler(Filters.location & not_start, self.shop_location), MessageHandler(Filters.all & not_start, self.incorrect_shop_location)],
                PASSPORT_PHOTO: [MessageHandler(Filters.photo & not_start, self.passport_photo), MessageHandler(Filters.all & not_start, self.invalid_passport_photo)],
                SHOP: [MessageHandler(Filters.text, self.shop)],
                SHOP_PASSPORT_PHOTO: [MessageHandler(Filters.photo & not_start, self.shop_passport_photo), MessageHandler(Filters.all & not_start, self.invalid_shop_passport_photo)],
                
                MENU: [
                    MessageHandler(Filters.regex("^(Kvitansiya|Квитанция)"), self.cvitation),
                    MessageHandler(Filters.regex("^(Mening ballarim|Мои баллы)"), self.my_balls),
                    CommandHandler('language', self.change_language),
                ],
                CVI_PHOTO: [MessageHandler(Filters.photo, self.cvi_photo), MessageHandler(Filters.regex("^(Mening ballarim|Мои баллы)"), self.my_balls), MessageHandler(Filters.regex("^(Kvitansiya|Kvitansiya)"), self.cvitation), ],
                CVI_SERIAL_NUMBER: [MessageHandler(Filters.text & not_start, self.cvi_serial_number), MessageHandler(Filters.regex("^(Kvitansiya|Kvitansiya)"), self.cvitation), MessageHandler(Filters.regex("^(Mening ballarim|Мои баллы)"), self.my_balls), ],
                BALL: [CallbackQueryHandler(self.my_balls, pattern="^gift_pagination"), CallbackQueryHandler(self.select_gift, pattern="^select_gift"), CallbackQueryHandler(self.selct_gift_sure, pattern="^sure_select_gift"), CallbackQueryHandler(self.start, pattern="^back")],
                SELECT_NEW_LANGUAGE: [MessageHandler(
                    Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.new_language)
                    ]

            },
            fallbacks=[CommandHandler("start", self.start), MessageHandler(Filters.all, self.start)],
        )
        self.dispatcher.add_handler(self.conversation)
        self.start_polling()
        print('polling')

        server = Flask(__name__)
        print('x')

        server.route('/delete_seller',
                     methods=['POST', 'GET'])(self.delete_seller)
        server.route('/reject_check',
                     methods=['POST', 'GET'])(self.reject_ball)
        

        server.run("127.0.0.1", port=6003)
    



    def reject_ball(self):
        data = request.get_json()
        if data:
            data = data['data']
            seller: Seller = Seller.objects.filter(id=data['id']).first()
            if seller:
                try:
                    self.bot.send_message(chat_id=  seller.chat_id,text=seller.text("reject_check_text").format(serial=data['serial'], ball=data['ball']))
                except:
                    pass
            return 'ok'
        return 'error'


    def delete_seller(self):
        data = request.get_json()
        if data:
            data = data['data']
            seller:Seller = Seller.objects.filter(id=data['id']).first()
            self.bot.send_message(chat_id=seller.chat_id, text=seller.text('you_are_deleted'), reply_markup=ReplyKeyboardRemove())
            seller.delete()
            return 'ok'
        return 'error'
        
        
    @delete_tmp_message
    def cvitation(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        context.user_data['tmp_message'] = user.send_message(
            i18n("send_cvitation",db_user.language))
        return CVI_PHOTO
    
    def cvi_photo(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        img = update.message.photo[-1].get_file().download(f"./media/cvitations/{str(uuid4())}.jpg")
        context.user_data['cvitation_img'] = img
        context.user_data['tmp_message'] = user.send_message(
            i18n("send_cvi_serial_number",db_user.language), reply_markup=ReplyKeyboardRemove())
        return CVI_SERIAL_NUMBER
    
    def cvi_serial_number(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        product = BaseProduct.objects.filter(serial_number=update.message.text)
        if product.exists():
            product:BaseProduct = product.first()
            if not product.is_active:
                Cvitation.objects.create(seller=db_user, serial=update.message.text, img=context.user_data['cvitation_img'])
                user.send_message(db_user.text("cvitation_success"))
                product.sale()
                db_user.balls += product.product.seller_ball
                db_user.save()
                try:
                    requests.get("http://127.0.0.1:6002/sale", json={"data": {
                        "serial_number":update.message.text,
                        "username":user.username,
                        "name":db_user.name,
                        "number":db_user.number,
                        "region":db_user.region.uz_data,
                    }})
                except Exception as e:
                    print(e)
                return self.start(update, context,False)
            else:
                user.send_message(db_user.text("already_sold"))
                return CVI_SERIAL_NUMBER
        else:
            if 'tmp_message' in context.user_data:
                try:
                    context.user_data['tmp_message'].delete()
                except:
                    pass
                try:
                    update.message.delete() if update.message else update.callback_query.message.delete()
                except:
                    pass
            context.user_data['tmp_message'] = user.send_message(db_user.text("seria_not_found"))
        return CVI_SERIAL_NUMBER
    
    def my_balls(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.message:
            if 'tmp_message' in context.user_data:
                try:
                    context.user_data['tmp_message'].delete()
                except:
                    pass
                try:
                    update.message.delete() if update.message else update.callback_query.message.delete()
                except:
                    pass
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
                    update.callback_query.answer(db_user.text("not_enough_balls"))
    def selct_gift_sure(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        data = update.callback_query.data.split(":")
        if data[0] == "sure_select_gift":
            if data[1] == "yes":
                context.user_data['current_gift'].take(db_user)
                update.callback_query.message.edit_text(db_user.text("accept_your_prompt"))
                return self.start(update, context, False)
            else:
                return self.my_balls(update, context)
    
    @delete_tmp_message
    def change_language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        update.message.reply_text()
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
        context.user_data['register']['language'] = lang = 0 if update.message.text.startswith(
            "🇺🇿") else (1 if update.message.text.startswith("🇷🇺") else None)
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


    @delete_tmp_message
    def incorrect_shop_location(self, update: Update, context: CallbackContext):
        context.user_data['tmp_message'] = update.message.reply_text(i18n("incorrect_shop_location", context.user_data['register']['language']), reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(i18n('request_location', context.user_data['register']['language']),request_location=True)]], resize_keyboard=True))
        return SHOP_LOCATION


    @delete_tmp_message
    def invalid_passport_photo(self, update: Update, context: CallbackContext):
        context.user_data['tmp_message'] = update.message.reply_text(i18n(
            "invalid_passport_photo", context.user_data['register']['language']), reply_markup=ReplyKeyboardRemove())
        return PASSPORT_PHOTO


    @delete_tmp_message
    def invalid_shop_passport_photo(self, update: Update, context: CallbackContext):
        context.user_data['tmp_message'] = update.message.reply_text(i18n("invalid_shop_passport_photo",
                                  context.user_data['register']['language']), reply_markup=ReplyKeyboardRemove())
        return SHOP_PASSPORT_PHOTO



from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Bot()
