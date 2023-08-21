from uuid import uuid4
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from admin_panel.models import District, Regions, Text, i18n
from seller.management.commands.constant import DILLERS_CHOICE, DISTRICT, LANGUAGE, MENU, NAME, NUMBER, PASSPORT_PHOTO, REGION, SHOP, CARD, SHOP_PASSPORT_PHOTO
from django.core.files.images import ImageFile
from seller.management.commands.decorators import delete_tmp_message, distribute, get_user
from seller.models import Seller
from diller.models import Diller

class MainHandlers:
    def start(self, update: Update, context: CallbackContext, delete=None):
        user, db_user = get_user(update)
        if delete and db_user:
            try:
                update.message.delete() if update.message else update.callback_query.message.delete()
            except: pass
            if 'tmp_message' in context.user_data:
                try:
                    context.user_data['tmp_message'].delete()
                except:pass
        
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
            if db_user.status == 1:
                context.user_data['tmp_message'] = user.send_message("menu", reply_markup=ReplyKeyboardMarkup(
                    distribute([db_user.text("cvitation"), db_user.text('my_balls'),db_user.text("score")], 2), resize_keyboard=True
                ), parse_mode="HTML")
                return MENU
            elif db_user.status == 0:
                user.send_message(i18n(
                "wait_accept", db_user.language), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
                return MENU
            elif db_user.status == 3:
                user.send_message(i18n(
                "block", db_user.language), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
                return MENU
                
            else:
                user.send_message(i18n(
                "not_access", db_user.language), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
                return MENU
                

        


    @delete_tmp_message
    def language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['language'] = lang = 0 if update.message.text.startswith(
            "🇺🇿") else (1 if update.message.text.startswith("🇷🇺") else 1)
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
        if not len(name.split()) > 1:
            context.user_data['tmp_message'] = update.message.reply_text(
                i18n("invalid_name", lang))
            return NAME
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
            context.user_data['tmp_message'] = user.send_message(i18n("shop_location",lang), reply_markup=ReplyKeyboardMarkup([[KeyboardButton(i18n('request_location', lang),request_location=True)]], resize_keyboard=True), parse_mode="HTML")
            return CARD
        else:
            context.user_data['keyboard_button'] = context.user_data['tmp_message'] = user.send_message("district_not_found", reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in District.objects.filter(region=context.user_data['register']['region'])
                ], 2), resize_keyboard=True
            ), parse_mode="HTML")
            return DISTRICT
    @delete_tmp_message
    def shop(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        context.user_data['register']['shop'] = update.message.text
        context.user_data['tmp_message'] = user.send_message(
            i18n('shop_passport_photo', lang))
        return SHOP_PASSPORT_PHOTO
    
    @delete_tmp_message
    def shop_location(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        context.user_data['register']['shop_location'] = {
            "latitude":update.message.location.latitude,
            "nongtitude":update.message.location.longitude
        }
        # db_user: Seller = Seller.objects.create(
        #     **context.user_data['register'])
        context.user_data['tmp_message'] = user.send_message(
            (i18n("passport_photo", lang)))
        return PASSPORT_PHOTO
    
    @delete_tmp_message
    def passport_photo(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        
        context.user_data['register']['passport_photo'] = ImageFile(
            open(update.message.photo[-1].get_file().download(f"./media/passport_photo/{str(uuid4())}.jpg"), 'rb'))
        context.user_data['tmp_message'] = user.send_message(i18n(
            "shop_name", lang), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        return SHOP
    
    @delete_tmp_message
    def shop_passport_photo(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        context.user_data['register']['shop_passport_photo'] = ImageFile(
            open(update.message.photo[-1].get_file().download(f"./media/passport_photo/{str(uuid4())}.jpg"), 'rb'))
        dillers = Diller.objects.filter(status=1)
        keyboard = [KeyboardButton(i.name) for i in dillers]
        
        user.send_message(i18n(
            "dillers_choice", lang), reply_markup=ReplyKeyboardMarkup(distribute(keyboard,3),resize_keyboard=True), parse_mode="HTML")
        context.user_data["dillers"] = []
        return DILLERS_CHOICE

    def dillers_choice(self,update:Update,context:CallbackContext):
        msg = update.message.text
        lang = context.user_data['register']['language']
        user, db_user = get_user(update)
        if msg == i18n("next", lang):
            db_user: Seller = Seller.objects.create(**context.user_data['register'])
            for i in context.user_data["dillers"]:
                db_user.dillers.add(i)
            user.send_message(i18n(
            "wait_accept", lang), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            return MENU
        diller = Diller.objects.filter(name=msg)
        if not diller:
            user.send_message(i18n(
            "diller_not_found", lang), parse_mode="HTML")
            return DILLERS_CHOICE
        
        context.user_data["dillers"].append(diller.first())
        dillers = Diller.objects.filter(status=1)
        keyboard =[KeyboardButton(i18n("next", lang))]
        for i in dillers:
            if i not in  context.user_data["dillers"]:
                keyboard.append(KeyboardButton(i.name))
        user.send_message(i18n(
            "dillers_choice_again", lang), reply_markup=ReplyKeyboardMarkup(distribute(keyboard,3),resize_keyboard=True), parse_mode="HTML")

        # db_user: Seller = Seller.objects.create(
        #     **context.user_data['register'])
        # return self.start(update,context)
