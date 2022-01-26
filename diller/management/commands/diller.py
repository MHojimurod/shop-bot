from tokenize import Number
from telegram.ext import *
from telegram import *
from diller.management.commands.constant import *
from diller.management.commands.decorators import distribute, get_user
from diller.models import Diller
from admin_panel.models import District, Regions, Text, i18n





user: User = None
db_user: Diller = None




class Bot(Updater):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler('start',self.start)
                ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)"), self.language)],
                NAME: [MessageHandler(Filters.text, self.name)],
                NUMBER: [MessageHandler(Filters.contact, self.number)],
                REGION: [MessageHandler(Filters.text, self.region)],
                DISTRICT: [MessageHandler(Filters.text, self.district)],
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(self.conversation)

        self.start_polling()
        print('polling')
        self.idle()
    

    def start(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register'] = {
            "chat_id": user.id,
        }
        if db_user is None:
            user.send_message(text=Text.objects.filter(name='start').first().uz_data, reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ],
                resize_keyboard=True
            ))
            return LANGUAGE
        else:
            user.send_message("menu", reply_markup=ReplyKeyboardMarkup(
                distribute([db_user.text("Buy"), db_user.text("taken"), db_user.text('my_balls')], 2)
            ))
            return MENU

    def language(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['language'] = lang = 0 if update.message.text.startswith("🇺🇿") else (1 if update.message.text.startswith("🇷🇺") else None)
        if lang is not None:
            user.send_message(i18n("request_name", lang), reply_markup=ReplyKeyboardRemove())
            return NAME
        else:
            user.send_message("language_not_found", reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ]
            ))
            return LANGUAGE

    def name(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['name'] = name = update.message.text
        lang = context.user_data['register']['language']
        user.send_message(i18n("request_number", lang), reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(i18n("send_number", lang), request_contact=True),
                    ]
                ]
            ))
        return NUMBER
    

    def number(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        context.user_data['register']['number'] = number = update.message.contact.phone_number
        lang = context.user_data['register']['language']
        user.send_message(i18n("select_region", lang), reply_markup=ReplyKeyboardMarkup(
            distribute([
                region.name(lang) for region in Regions.objects.all()
            ], 2)
        ))
        return REGION
    
    def region(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        region = Regions.objects.filter(**{ "uz_data" if lang == 0 else "ru_data": update.message.text}).first()
        if region:
            context.user_data['register']['region'] = region
            user.send_message("select_district", reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in District.objects.filter(region=region)
                ], 2)
            ))
            return DISTRICT

        else:
            user.send_message("region_not_found", reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in Regions.objects.all()
                ], 2)
            ))
            return REGION

    def district(self, update:Update, context:CallbackContext):
        user, db_user = get_user(update)
        lang = context.user_data['register']['language']
        district = District.objects.filter(**{ "uz_data" if lang == 0 else "ru_data": update.message.text}).first()
        if district:
            context.user_data['register']['district'] = district
            db_user:Diller = Diller.objects.create(**context.user_data['register'])
            user.send_message("select_district", reply_markup=ReplyKeyboardMarkup(
                distribute([db_user.text("Buy"), db_user.text("taken"), db_user.text('my_balls')], 2)
            ))
            return MENU
        else:
            user.send_message("district_not_found", reply_markup=ReplyKeyboardMarkup(
                distribute([
                    region.name(lang) for region in District.objects.filter(region=context.user_data['register']['region'])
                ], 2)
            ))
            return LANGUAGE
            
    
bot = Bot(TOKEN)