from datetime import datetime
from uuid import uuid4
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from admin_panel.models import Regions
from seller.management.commands.constant import (
    LANGUAGE,
    MENU,
    NAME,
    NUMBER,
    REGION,

)
from django.core.files.images import ImageFile
from sale.management.commands.decorators import delete_tmp_message, distribute, get_user

from sale.models import Cashback, SaleSeller


def is_user_following(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(e)
        return False


class MainHandlers:
    def start(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)

        is_member = is_user_following(self.bot, 2045594351, user.id)



        if update.callback_query and update.callback_query.data == 'start':
            try:
                update.callback_query.message.delete()
            except:
                pass
            user.send_message("Kechirasiz siz kanalga obuna bo'lmagansiz.\n\nIltimos shu kanalga obuna bo'ling.", reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "Obuna bo'lish ➕", url="https://t.me/ELITE_aksiya")
                ],
                [
                    InlineKeyboardButton(
                        "Obuna bo'ldim ✅", callback_data='start')
                ]
            ]))
            return


        if not is_member:

            user.send_message("Iltimos shu kanalga obuna bo'ling.", reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "Obuna bo'lish ➕", url="https://t.me/ELITE_aksiya")
                ],
                [
                    InlineKeyboardButton(
                        "Obuna bo'ldim ✅", callback_data='start')
                ]
            ]))
            return




        if not db_user.language:
            user.send_message(
                f"Salom {user.first_name}",
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
            text = {
                "uz": "Ismingizni kiriting",
                "ru": "Введите ваше имя"
            }
            user.send_message(
                text=text[db_user.language],
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML",
            )
            return NAME
        elif not db_user.phone:
            text = {
                "uz": "Telefon raqamizni kiriting",
                "ru": "Введите свой номер телефона"
            }
            send_btn = {
                "uz": "Yuborish",
                "ru": "Отправить"
            }
            user.send_message(text=text[db_user.language],
                              reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            send_btn[db_user.language], request_contact=True),
                    ]
                ],
                resize_keyboard=True,
            ),
                parse_mode="HTML",
            )
            return NUMBER
        elif not db_user.region:
            text = {
                "uz": "Viloyatingizni tanlang",
                "ru": "Выберите свой регион"
            }
            user.send_message(text=text[db_user.language],
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
            seria = {
                "uz": "Seriya № yuborish",
                "ru": "Отправить серийный номер"
            }
            my_account = {
                "uz": "Mening hisobim",
                "ru": "Мой счет"
            }
            help_btn = {
                "uz": "Yordam",
                "ru": "Помощь"
            }
            promo = {
                "uz": "Proma kodni kiritish",
                "ru": "Введите промокод"
            }
            prizes = {
                "uz": "Yutuqlar",
                "ru": "Достижения"
            }
            button = [
                [KeyboardButton(promo[db_user.language])],
                [
                    #KeyboardButton(seria[db_user.language]),
                 prizes[db_user.language]],
                [
                    #KeyboardButton(my_account[db_user.language]),
                 KeyboardButton(help_btn[db_user.language])],
            ]
            user.send_message(
                "Menu",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                parse_mode="HTML",
            )
            return MENU
        elif db_user.state == SaleSeller.WAITING:
            help_btn = {
                "uz": "Yordam",
                "ru": "Помощь"
            }
            button = [[KeyboardButton(help_btn[db_user.language])]]
            user.send_message(
                "Kuting",
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                parse_mode="HTML",
            )
            return MENU
        elif db_user.state == SaleSeller.CANCELED:
            help_btn = {
                "uz": "Yordam",
                "ru": "Помощь"
            }
            button = [[KeyboardButton(help_btn[db_user.language])]]
            text = {
                "uz": "Sizning so'rovingiz bekor qilingan",
                "ru": "Ваш запрос отменен"
            }
            user.send_message(
                text=text[db_user.language],
                reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
            )
            return MENU

    def language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        lang = (
            "uz"
            if update.message.text.startswith("🇺🇿")
            else ("ru" if update.message.text.startswith("🇷🇺") else "ru")
        )
        db_user.set_language(lang)

        if db_user.language:
            text = {
                "uz": "Ismingizni kiriting",
                "ru": "Введите ваше имя"
            }
            user.send_message(text=text[db_user.language],
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode="HTML",
                              )
            return NAME
        else:
            user.send_message(
                "Til Topilmadi",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                    ],
                    resize_keyboard=True,
                ),
                parse_mode="HTML",
            )
            return LANGUAGE

    def name(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        name = update.message.text
        db_user.set_name(name)

        text = {
            "uz": "Telefon raqamizni kiriting",
            "ru": "Введите свой номер телефона"
        }
        send_btn = {
            "uz": "Yuborish",
            "ru": "Отправить"
        }

        user.send_message(text=text[db_user.language],
                          reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        send_btn[db_user.language], request_contact=True),
                ]
            ],
            resize_keyboard=True,
        ),
            parse_mode="HTML",
        )
        return NUMBER

    def number(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        phone = None
        if update.message.text:
            phone = update.message.text
        elif update.message.contact.phone_number:
            phone = update.message.contact.phone_number
        db_user.set_phone(phone)
        db_user.save()
        text = {
            "uz": "Viloyatingizni tanlang",
            "ru": "Выберите свой регион"
        }
        user.send_message(text=text[db_user.language],
                          reply_markup=ReplyKeyboardMarkup(
            distribute(
                [region.name(db_user.language)
                 for region in Regions.objects.all()],
                2,
            ),
            resize_keyboard=True,
        ),
            parse_mode="HTML",
        )
        return REGION

    def region(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        msg = update.message.text
        region = Regions.objects.filter(
            **{"uz_data" if db_user.language == "uz" else "ru_data": msg}
        )
        if region.exists():
            help_btn = {
                "uz": "Yordam",
                "ru": "Помощь"
            }
            text = {
                "uz": "Tasdiqlanishingiz kutilmoqda",
                "ru": "Ваше подтверждение ожидает"
            }
            db_user.set_region(region.first())
            button = [[KeyboardButton(help_btn[db_user.language])]]
            user.send_message(text=text[db_user.language],
                              reply_markup=ReplyKeyboardMarkup(
                                  button, resize_keyboard=True),
                              )
            return MENU

        else:
            text = {
                "uz": "Viloyat topilmadi",
                "ru": "Регион не найден"
            }
            user.send_message(text=text[db_user.language],
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
        seria.is_used = True
        seria.seller = db_user
        seria.used_time = datetime.now().date()
        seria.save()
        db_user.save()
        cashback = Cashback.objects.create(
            photo=photo.name.replace("./media/", ''), seria=seria)
        help_btn = {
            "uz": "Yordam",
            "ru": "Помощь"
        }
        seria = {
            "uz": "Seriya № yuborish",
            "ru": "Отправить серийный номер"
        }
        my_account = {
            "uz": "Mening hisobim",
            "ru": "Мой счет"
        }
        button = [
            [KeyboardButton(seria[db_user.language])],
            [KeyboardButton(my_account[db_user.language]),
             KeyboardButton(help_btn[db_user.language])],
        ]
        text = {
            "uz": f"Tabriklaymiz hizobingizga ${cashback.seria.cashback} cashback tushirildi",
            "ru": f"Поздравляем, кешбэк ${cashback.seria.cashback} добавлен на ваш счет."
        }
        update.message.reply_html(text=text[db_user.language],
                                  reply_markup=ReplyKeyboardMarkup(
                                      button, resize_keyboard=True),
                                  )

        return MENU
