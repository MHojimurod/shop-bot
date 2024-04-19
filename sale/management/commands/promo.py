
from io import BytesIO
from telegram.ext import (
    Filters,
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
)

from telegram import (
    ReplyKeyboardMarkup,
    Update,
)
from sale.management.commands.decorators import get_user

from sale.models import PromoCode, PromocodeRequest

from .constant import (
    ACCOUNT,
    BACK,
    CASHBACK,
    CASHBACK_PHOTO,
    LANGUAGE,
    SALE_PROMOCODE,
    SALE_PROMOCODE_IMAGE,
    SELECT_NEW_LANGUAGE,
    HOLDER,
    TOKEN,
    NUMBER,
    NAME,
    REGION,
    MENU,
    CARD,
)

from django.core.files.base import File
from django.utils import timezone


class PromoAction:
    def promoActionHandlers(self):
        return ConversationHandler(
            [
                MessageHandler(Filters.regex(
                    "^(Proma kodni kiritish|Введите промокод)"), self.enter_promo),
                MessageHandler(Filters.regex(
                    "^(Yutuqlar|Достижения)"), self.gifts),

            ],
            {
                SALE_PROMOCODE: [
                    MessageHandler(Filters.regex(r"\d{5}"),self.enter_promo_code)
                ],
                SALE_PROMOCODE_IMAGE:[
                    MessageHandler(Filters.photo, self.enter_promo_code_image)
                ]
            },
            [
                CommandHandler('start', self.start)
            ],
            allow_reentry=True,
            name="promoActionHandler"
        )

    # @delete_tmp_message
    def enter_promo(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        t = {
            "uz": "Iltimos promokodni yuboring.",
            "ru": "Пожалуйста, пришлите промокод."
        }
        user.send_message(
            t.get(db_user.language),
            reply_markup=ReplyKeyboardMarkup([
                [BACK.get(db_user.language)],
            ],True)
        )

        return SALE_PROMOCODE


    # @delete_tmp_message
    def enter_promo_code(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)


        code = int(update.message.text)


        promo = PromoCode.objects.filter(code=code).first()

        if not promo:
            t = {
                "uz": "Kechirasiz promocode topilmadi.",
                "ru": "Извините, промокод не найден."
            }
            user.send_message(t[db_user.language])
            return self.enter_promo(update,context)






        if promo.status == 1:
            print(user)
            t = {
                "uz": "Kechirasiz bu promokodni ishlatolmaysiz.",
                "ru": "К сожалению, вы не можете использовать этот промокод.",

            }
            user.send_message(t[db_user.language])
            return self.enter_promo(update,context)


        if promo.status == 3:
            print(promo.status)
            t = {
                "uz": "Kechirasiz promokod ishlatilgan.",
                "ru": "Извините, был использован промокод."
            }
            user.send_message(t[db_user.language])
            return self.enter_promo(update,context)



        if db_user.diller == None:
            db_user.diller = promo.diller
            db_user.save()
        else:
            if db_user.diller != promo.diller:

                t = {
                "uz": "Kechirasiz siz bu diller bilan ishlamaysiz.",
                "ru": "К сожалению, вы не работаете с этим дилером."
            }
                user.send_message(t[db_user.language])
                return self.enter_promo(update,context)






        db_user.last_promocode = promo
        db_user.save()


        t = {
                "uz": "Iltimos stikerni rasmini yuboring.",
                "ru": "Пожалуйста, пришлите изображение наклейки."
            }
        user.send_message(t[db_user.language])

        return SALE_PROMOCODE_IMAGE





    # @delete_tmp_message
    def enter_promo_code_image(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)



        promo = db_user.last_promocode

        image= update.message.photo[-1]

        file = image.get_file()


        out = BytesIO()
        file.download(out=out)


        t = {
                "uz": f"Promokodingiz qabul qilindi.\n\nPromocodning harfi: {promo.letter}",
                "ru": f"Ваш промокод принят.\n\nPromocodning harfi: {promo.letter}"
            }
        user.send_message(t[db_user.language])

        extension = file.file_path.split(".")[-1]


        promo_request = PromocodeRequest.objects.create(
            seller=db_user,
            promo=promo,
            image=File(out,f"promo_{promo.seria}.{extension}")
        )




        promo.status = 3
        promo.seller = db_user

        promo.image = File(out,f"promo_{promo.seria}.{extension}")
        promo.save()






        # self.give_promo(update,context)
        promo.give_promo(promo_request, db_user)











        t = {
                "uz": "Promocode qabul qilindi.\n\nTasdiqlanganda sizga habar beramiz.",
                "ru": "Промокод принят."
            }
        user.send_message(t[db_user.language])


        return self.start(update,context)











    # @delete_tmp_message
    def gifts(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)



        if db_user.gifts.count() < 1:
            t = {
                "uz": f"Kechirasiz sizning yutuqlaringiz yo'q. Promocodlarni ro'yxatdan o'tqazing.",
                "ru": f"Извините, у вас нет достижений. Зарегистрируйте промокоды."
            }
            user.send_message(t[db_user.language])
            return self.start(update,context)

        gifts_text = db_user.gifts_text("\n").upper()



        t = {
                "uz": f"Sizning yutuqlaringiz.\n\n{gifts_text}",
                "ru": f"Ваши достижения.\n\n{gifts_text}"
            }
        user.send_message(t[db_user.language])

        return self.start(update,context)






