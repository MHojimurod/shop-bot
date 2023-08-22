from uuid import uuid4
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from admin_panel.models import District, Regions, Text, i18n
from seller.management.commands.constant import (
    DILLERS_CHOICE,
    DISTRICT,
    LANGUAGE,
    MENU,
    NAME,
    NUMBER,
    PASSPORT_PHOTO,
    REGION,
    SHOP,
    CARD,
    SHOP_PASSPORT_PHOTO,
)
from django.core.files.images import ImageFile
from sale.management.commands.decorators import delete_tmp_message, distribute, get_user
from seller.models import Seller
from diller.models import Diller
from sale.models import Cashback, SaleSeller, Card


class MainHandlers:
    def start(self, update: Update, context: CallbackContext, delete=None):
        user, db_user = get_user(update)
        if not db_user.language:
            context.user_data["keyboard_button"] = context.user_data[
                "tmp_message"
            ] = user.send_message(
                "Hello",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                    ],
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return LANGUAGE
        elif not db_user.name:
            user.send_message(
                "Ismingizni kiriting",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML",
            )
            return NAME
        elif not db_user.phone:
            user.send_message(
                "Tel raqamizni kiriting",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            KeyboardButton("Yuborish", request_contact=True),
                        ]
                    ],
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return NUMBER
        elif not db_user.region:
            user.send_message(
                "Viloyatingizni tanlang",
                reply_markup=ReplyKeyboardMarkup(
                    distribute(
                        [
                            region.name(db_user.language)
                            for region in Regions.objects.all()
                        ],
                        2,
                    ),
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return REGION
        if db_user.state == SaleSeller.ACCEPT:
            button = [
                [KeyboardButton("CashBack olish")],
                [KeyboardButton("Mening hisobim"), KeyboardButton("Yordam")],
            ]
            user.send_message(
                "menu",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                parse_mode="HTML",
            )
            return MENU
        elif db_user.state == SaleSeller.WAITING:
            button = [[KeyboardButton("Yordam")]]
            user.send_message(
                "Kuting",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                parse_mode="HTML",
            )
            return MENU
        elif db_user.state == SaleSeller.CANCELED:
            button = [[KeyboardButton("Yordam")]]
            user.send_message(
                "Bekor qilindingiz",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
            )
            return MENU

    @delete_tmp_message
    def language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = (
            "uz"
            if update.message.text.startswith("🇺🇿")
            else ("ru" if update.message.text.startswith("🇷🇺") else "ru")
        )
        db_user.set_language(lang)

        if db_user.language:
            user.send_message(
                "Ismingizni kiriting",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML",
            )
            return NAME
        else:
            user.send_message(
                "language_not_found",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                    ],
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return LANGUAGE

    # @delete_tmp_message
    def name(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        name = update.message.text
        db_user.set_name(name)

        user.send_message(
            "Tel raqamizni kiriting",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton("Yuborish", request_contact=True),
                    ]
                ],
                resize_keyboard=True,
            ),
            parse_mode="HTML",
        )
        return NUMBER

    # @delete_tmp_message
    def number(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        phone = None
        if update.message.text:
            phone = update.message.text
        elif update.message.contact.phone_number:
            phone = update.message.contact.phone_number
        db_user.set_phone(phone)
        db_user.save()
        user.send_message(
            "Viloyatingizni tanlang",
            reply_markup=ReplyKeyboardMarkup(
                distribute(
                    [region.name(db_user.language) for region in Regions.objects.all()],
                    2,
                ),
                resize_keyboard=True,
            ),
            parse_mode="HTML",
        )
        return REGION

    @delete_tmp_message
    def region(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        msg = update.message.text
        region = Regions.objects.filter(
            **{"uz_data" if db_user.language == "uz" else "ru_data": msg}
        )
        print(msg)
        if region.exists():
            db_user.set_region(region.first())
            button = [[KeyboardButton("Yordam")]]
            user.send_message(
                "Tasdiqlanishingiz kutilmoqda",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
            )
            return MENU

        else:
            user.send_message(
                "Viloyat topilmadi",
                reply_markup=ReplyKeyboardMarkup(
                    distribute(
                        [
                            region.name(db_user.language)
                            for region in Regions.objects.all()
                        ],
                        2,
                    ),
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return REGION

    def cashback_photo(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        photo = ImageFile(
            open(
                update.message.photo[-1]
                .get_file()
                .download(f"./media/cashback/{str(uuid4())}.jpg"),
                "rb",
            )
        )
        seria = context.user_data.get("seria", None)
        print(seria)
        seria.is_used = True
        seria.seller = db_user
        db_user.account += seria.cashback
        seria.save()
        db_user.save()
        cashback = Cashback.objects.create(photo=photo.name.replace("./media/", ''), seria=seria)
        button = [
            [KeyboardButton("CashBack olish")],
            [KeyboardButton("Mening hisobim"), KeyboardButton("Yordam")],
        ]
        update.message.reply_html(
            f"Tabriklaymiz hizobingizga ${cashback.seria.cashback} cashback tushirildi",
            reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
        )

        return MENU
