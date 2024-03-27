
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
from seller.models import Seller

from .constant import (
    ACCOUNT,
    BACK,
    CASHBACK,
    CASHBACK_PHOTO,
    LANGUAGE,
    SALE_PROMOCODE,
    SELECT_NEW_LANGUAGE,
    HOLDER,
    TOKEN,
    NUMBER,
    NAME,
    REGION,
    MENU,
    CARD,
)


class PromoAction:
    def promoActionHandlers(self):
        return ConversationHandler(
            [
                MessageHandler(Filters.regex(
                    "^(Proma kodni kiritish|Введите промокод)"), self.enter_promo)
            ],
            {
                SALE_PROMOCODE: [
                    MessageHandler(Filters.regex(r"\d{5}"),self.enter_promo_code)
                ]
            },
            [
                CommandHandler('start', self.start)
            ],
            allow_reentry=True,
            name="promoActionHandler"
        )

    @delete_tmp_message
    def enter_promo(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        t = {
            "uz": "Iltimos promokodni yuboring.",
            "ru": "Пожалуйста, пришлите промокод."
        }
        user.send_message(
            t.get(db_user.language),
            reply_markup=ReplyKeyboardMarkup([
                BACK.get(db_user.language)
            ])
        )

        return SALE_PROMOCODE


    @delete_tmp_message
    def enter_promo_code(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)


        code = int(update.message.text)

        
