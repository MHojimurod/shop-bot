
from telegram.ext import (
    Updater,
    Filters,
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
)

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    User,
)
from admin_panel.models import Text
from diller.management.commands.decorators import delete_tmp_message
from sale.management.commands.decorators import get_user

from sale.models import Card, CashOrder, SerialNumbers
from seller.models import  Seller

from .constant import (
    ACCOUNT,
    CASHBACK,
    CASHBACK_PHOTO,
    LANGUAGE,
    SELECT_NEW_LANGUAGE,
    HOLDER,
    TOKEN,
    NUMBER,
    NAME,
    REGION,
    MENU,
    CARD,
)


from sale.stages import MainHandlers

user: User = None
db_user: Seller = None

back = {
    "uz": "Ortga",
    "ru": "Назад"
}


class Bot(Updater, MainHandlers):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        not_start = ~Filters.regex("^(/start)")

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.start),
            ],
            states={
                LANGUAGE: [
                    MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)
                ],
                NAME: [MessageHandler(Filters.text & not_start, self.name)],
                NUMBER: [
                    MessageHandler(Filters.contact & not_start, self.number),
                    MessageHandler(Filters.regex("^(\+998\d{9})$"), self.number),
                    MessageHandler(Filters.all & not_start, self.invalid_number),
                ],
                REGION: [
                    MessageHandler(Filters.text & not_start, self.region),
                ],
                ACCOUNT: [
                    MessageHandler(
                        Filters.regex("^(Kartaga chiqarish|Выпуск на карту)"), self.transfer
                    ),
                    MessageHandler(Filters.regex("^(Ortga|Назад)"), self.start),
                ],
                CARD: [
                    MessageHandler(Filters.regex("^(\d{16})$"), self.card),
                    MessageHandler(Filters.regex("^(Ortga|Назад)"), self.my_account),
                    MessageHandler(Filters.text & not_start, self.invalid_card),
                ],
                HOLDER: [
                    MessageHandler(Filters.regex("^(Ortga|Назад)"), self.transfer),
                    MessageHandler(Filters.text & not_start, self.holder_name),
                ],
                CASHBACK_PHOTO: [
                    MessageHandler(Filters.photo & not_start, self.cashback_photo),
                ],
                MENU: [
                    MessageHandler(Filters.regex("^(Yordam|Помощь)"), self.help),
                    MessageHandler(Filters.regex("^(Seriya № yuborish|Отправить серийный номер)"), self.cashback),
                    MessageHandler(Filters.regex("^(Mening hisobim|Мой счет)"), self.my_account),
                    CommandHandler("language", self.change_language),
                ],
                CASHBACK: [
                    MessageHandler(Filters.regex("^(Ortga|Назад)"), self.start),
                    MessageHandler(Filters.text & not_start, self.check_cashback),
                ]
                
            },
            fallbacks=[
                CommandHandler("start", self.start),
                MessageHandler(Filters.all, self.start),
            ],
        )
        self.dispatcher.add_handler(self.conversation)
        self.start_polling()
        print("polling")
        self.idle()


    @delete_tmp_message
    def change_language(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        user.send_message(text=f"Salom {user.first_name}",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
                ],
                resize_keyboard=True,
            ),
            parse_mode="HTML",
        )
        return LANGUAGE


    def invalid_number(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        text = {
            "uz": "Nomerni xato kiritdingiz iltimos tekshirib qayta kiriting",
            "ru": "Вы неправильно ввели номер, проверьте и введите еще раз"
        }
        update.message.reply_text(text=text[db_user.language])
        return NUMBER

    def help(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        text = {
            "uz": "Hurmatli sotuvchi sizda ushbu aksiya bo'yicha murojaatlaringiz bo'lsa quydagi manzilarga etishingiz mumkin:\n\n☎️ +998557020020\nIsh vaqti: Dush-Shanba 8:00-18:00",
            "ru": "Уважаемый продавец, если у вас есть вопросы по данной акции, вы можете обращаться по следующим адресам:\n\n☎️ +998557020020\nРежим работы: Пн-Сб 8:00-18:00"
        }
        button = {
            "uz": "Telegram orqali",
            "ru": "Через Телеграм"
        }
        inline_button = [
            [InlineKeyboardButton(button[db_user.language], url="https://t.me/Farrukhuz")]
        ]

        update.message.reply_html(
            text=text[db_user.language], reply_markup=InlineKeyboardMarkup(inline_button)
        )
        return MENU

    def cashback(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        button = [[KeyboardButton(back[db_user.language])]]
        text = {
            "uz": "Stikerda joylashgan 7 ta raqamli seriya raqamni kiriting",
            "ru": "Введите семизначный серийный номер, указанный на наклейке"
        }
        update.message.reply_html(
            text[db_user.language],
            reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
        )
        return CASHBACK

    def check_cashback(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        text = update.message.text
        try:
            code = SerialNumbers.objects.get(code=text)
            if code.is_used:
                text = {
                    "uz": "Ushbu seria raqam allaqachon foydalanilgan",
                    "ru": "Этот серийный номер уже используется"
                }
                update.message.reply_html(text=text[db_user.language])
                return CASHBACK
            text = {
                "uz": "Stikerni himoya qatlamini o'chirib suratga oling va bizga yuboring",
                "ru": "Сфотографируйте наклейку со снятым защитным слоем и пришлите ее нам."
            }
            update.message.reply_html(text=text[db_user.language])
            context.user_data["seria"] = code
            return CASHBACK_PHOTO

        except:
            text = {
                "uz": "Bunday seria  raqam topilamdi",
                "ru": "Серийный номер не найден"
            }
            update.message.reply_html(text=text[db_user.language])
            return CASHBACK

    def my_account(self, update: Update, coxtext: CallbackContext):
        user, db_user = get_user(update)
        text = f"ID raqamingiz: #{db_user.pk}\n\n"
        text += f"Umumiy cashback summasi: ${db_user.total_sum}\n\n"
        text += f"To'langan: ${db_user.payed_sum}\n\n"
        text += f"Kutilyotgan: ${db_user.waiting_sum}\n\n"
        text += f"To'lovga tasdiqlangan: ${db_user.account}" 
        button = []
        if db_user.account >= 5:
            button_text = {
                "uz": "Kartaga chiqarish",
                "ru": "Выпуск на карту"
            }
            button.append([KeyboardButton(button_text[db_user.language])])
        button.append([KeyboardButton(back[db_user.language])])
        user.send_message(
            text=text, reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
        )
        return ACCOUNT

    def transfer(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        card = Card.objects.filter(seller=db_user).last()
        text = {
            "uz": "Bonus mablag'ini o'z hisobingizga  o'tkazish uchun HUMO yoki UZCARD kartangizning   16 talik hisob raqamini  yozing",
            "ru": "Для перевода бонусных средств на свой счет напишите 16-значный номер счета вашей карты HUMO или UZCARD"
        }
        button = []
        if card:
            button.append([KeyboardButton(card.card_number)])
            text["uz"]+= "\nYoki quyidagi karta raqamingizni tanlang"
            text["ru"]+= "\nИли выберите номер своей карты ниже"

        button.append([KeyboardButton("Ortga")])
        update.message.reply_html(
            text=text[db_user.language], reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
        )
        return CARD

    def card(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        text = update.message.text
        context.user_data["card"] = text
        card = Card.objects.filter(seller=db_user, card_number=text).last()
        if card:
            self.holder_name(update, context)
            return MENU
        button = [[KeyboardButton(back[db_user.language])]]
        text = {
            "uz": "Karta egasi ism familyasini kiriting",
            "ru": "Введите имя и фамилию владельца карты"
        }
        update.message.reply_html(text=text[db_user.language],
            reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
        )
        return HOLDER

    def invalid_card(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        text = {
            "uz": "Karta raxamt 16 xonali sondan iborat bo'lishi shart\n\nMasalan: xxxx xxxx xxxx xxxx",
            "ru": "Карта должна содержать 16-значный номер\n\nНапример: xxxx xxxx xxxx xxxx"
        }
        update.message.reply_html(text=text[db_user.language])
        return CARD

    def holder_name(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        msg = update.message.text
        card_number = context.user_data.get("card", None)
        card = Card.objects.filter(seller=db_user, card_number=card_number).last()
        if not card:
            card = Card.objects.create(
                card_number=card_number, holder_name=msg, seller=db_user
            )
        CashOrder.objects.create(seller=db_user, card=card, price=db_user.account)
        db_user.account= 0
        db_user.save()
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
            [KeyboardButton(my_account[db_user.language]), KeyboardButton(help_btn[db_user.language])],
        ]
        text = {
            "uz": "Kartangiz tasdiqlanishi  bilan sizga o'tkazib beramiz",
            "ru": "Как только ваша карта будет одобрена, мы передадим ее вам"
        }
        update.message.reply_html(text=text[db_user.language],
            reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
        )
        return MENU


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Bot(TOKEN)
