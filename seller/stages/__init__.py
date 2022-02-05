


from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from admin_panel.models import District, Regions, Text, i18n
from seller.management.commands.constant import DISTRICT, LANGUAGE, MENU, NAME, NUMBER, REGION, SHOP

from seller.management.commands.decorators import delete_tmp_message, distribute, get_user
from seller.models import Seller

class MainHandlers:
    def start(self, update: Update, context: CallbackContext, delete:bool=True):
        if delete:
            try:
                update.message.delete() if update.message else update.callback_query.message.delete()
            except: pass
            if 'tmp_message' in context.user_data:
                try:
                    context.user_data['tmp_message'].delete()
                except:pass
        
        user, db_user = get_user(update)
        context.user_data['register'] = {
            "chat_id": user.id,
        }
        context.user_data['buy'] = {}
        if db_user is None:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(text=Text.objects.filter(name='start').first().uz_data, reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ],
                resize_keyboard=True
            ), parse_mode="HTML")
            return LANGUAGE
        else:
                context.user_data['tmp_message'] = user.send_message("menu", reply_markup=ReplyKeyboardMarkup(
                    distribute([db_user.text("cvitation"), db_user.text('my_balls')], 2), resize_keyboard=True
                ), parse_mode="HTML")
                return MENU

    @delete_tmp_message
    def language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['language'] = lang = 0 if update.message.text.startswith(
            "🇺🇿") else (1 if update.message.text.startswith("🇷🇺") else None)
        if lang is not None:
            context.user_data['tmp_message'] = user.send_message(
                i18n("request_name", lang), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            return NAME
        else:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message("language_not_found", reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ], resize_keyboard=True
            ), parse_mode="HTML")
            return LANGUAGE

    @delete_tmp_message
    def name(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['name'] = name = update.message.text
        lang = context.user_data['register']['language']
        context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(i18n("request_number", lang), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(i18n("send_number", lang),
                                   request_contact=True),
                ]
            ], resize_keyboard=True
        ), parse_mode="HTML")
        return NUMBER

    @delete_tmp_message
    def number(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['number'] = number = update.message.contact.phone_number
        lang = context.user_data['register']['language']
        context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(i18n("select_region", lang), reply_markup=ReplyKeyboardMarkup(
            distribute([
                region.name(lang) for region in Regions.objects.all()
            ], 2), resize_keyboard=True
        ), parse_mode="HTML")
        return REGION

    @delete_tmp_message
    def region(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        region = Regions.objects.filter(
            **{"uz_data" if lang == 0 else "ru_data": update.message.text}).first()
        if region:
            context.user_data['register']['region'] = region
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(i18n("select_district",lang), reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in District.objects.filter(region=region)
                ], 2), resize_keyboard=True
            ), parse_mode="HTML")
            return DISTRICT

        else:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message(i18n("region_not_found",lang), reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in Regions.objects.all()
                ], 2), resize_keyboard=True
            ), parse_mode="HTML")
            return REGION

    @delete_tmp_message
    def district(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        district = District.objects.filter(
            **{"uz_data" if lang == 0 else "ru_data": update.message.text}).first()
        if district:
            context.user_data['register']['district'] = district
            # db_user: Seller = Seller.objects.create(
            #     **context.user_data['register'])
            # # context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message("select_district", reply_markup=ReplyKeyboardMarkup(
            # #     distribute([db_user.text("Buy"), db_user.text("taken"), db_user.text('my_balls')], 2), resize_keyboard=True
            # # ), parse_mode="HTML")
            # context.user_data['tmp_message'] = user.send_message("Ro'yhatdan o'tildi! endi ruhsat berilishini kuting!\n\n\Ruhsat berilganda o'zimiz habar beramiz yoki /start kommandasini yuboring", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            # return -1
            context.user_data['tmp_message'] = user.send_message("Iltimos endi do'kon nomini yozing!", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            return SHOP
        else:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message("district_not_found", reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in District.objects.filter(region=context.user_data['register']['region'])
                ], 2), resize_keyboard=True
            ), parse_mode="HTML")
            return LANGUAGE
    
    def shop(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        # lang = context.user_data['register']['language']
        context.user_data['register']['shop'] = update.message.text
        db_user: Seller = Seller.objects.create(
            **context.user_data['register'])
        self.start(update,context)
        # context.user_data['tmp_message'] = user.send_message("Ro'yhatdan o'tildi! endi ruhsat berilishini kuting!\n\n\Ruhsat berilganda o'zimiz habar beramiz yoki /startkommandasini yuboring", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        # return -1