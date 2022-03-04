
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update
)
from telegram.ext import (
    CallbackContext
)
from admin_panel.models import i18n, Gifts

from diller.management.commands.decorators import delete_tmp_message, get_user
from diller.models import Busket

from diller.utils import balls_keyboard_pagination, busket_keyboard, category_pagination_inline, diller_products_paginator
from ..management.commands.constant import BALL, CART, PURCHASED, SELECT_CATEGORY


class Menu:
    @delete_tmp_message
    def buy(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if update.message:
            context.user_data['current_busket'] = db_user.busket
            context.user_data['buy']['pagination'] = 1
            context.user_data['tmp_message'] = user.send_message(**category_pagination_inline(
                db_user.language, context.user_data['buy']['pagination'], context), parse_mode="HTML")
        elif update.callback_query:
            data = update.callback_query.data.split(":")
            if data[0] == "category_pagination":
                context.user_data['buy']['pagination'] = int(data[1])
                update.callback_query.message.edit_text(**category_pagination_inline(
                    db_user.language, context.user_data['buy']['pagination'], context))
            else:
                context.user_data['buy']['pagination'] = 1
                keyboard = category_pagination_inline(
                    db_user.language, context.user_data['buy']['pagination'], context)
                # update.callback_query.message.delete()
                context.user_data['tmp_message'] = user.send_message(
                    **keyboard, parse_mode="HTML")
        return SELECT_CATEGORY

    @delete_tmp_message
    def purchased(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if update.message:
            if len(db_user.products()) > 0:
                context.user_data['tmp_message'] = user.send_message(
                    **diller_products_paginator(db_user, 1), parse_mode="HTML")
            else:
                context.user_data['tmp_message'] = user.send_message(
                    db_user.text("no_orders"), parse_mode="HTML")
                return self.start(update, context, False)
        else:
            data = update.callback_query.data.split(":")
            if data[0] == "product_pagination":
                context.user_data['tmp_message'] = user.send_message(
                    **diller_products_paginator(db_user, int(data[1])), parse_mode="HTML")
        return PURCHASED

    # @delete_tmp_message
    delete_tmp_message

    def my_balls(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
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
            context.user_data['tmp_message'] = user.send_message(
                **balls_keyboard_pagination(db_user, 1), parse_mode="HTML")
            return BALL
        else:
            data = update.callback_query.data.split(":")
            if data[0] == "gift_pagination":
                update.callback_query.message.edit_text(
                    **balls_keyboard_pagination(db_user, int(data[1])), parse_mode="HTML")
                return BALL

    def select_gift(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        if data[0] == "select_gift":
            gift = Gifts.objects.filter(id=int(data[1]))
            if gift.exists():
                if gift.first().ball <= db_user.balls:
                    context.user_data['current_gift'] = gift.first()
                    update.callback_query.message.edit_text(i18n("are_you_sure_get_gift", db_user.language),    parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                i18n("yes", db_user.language), callback_data="sure_select_gift:yes"),
                            InlineKeyboardButton(
                                i18n("no", db_user.language), callback_data="sure_select_gift:no")
                        ]
                    ]))
                    return BALL
                else:
                    update.callback_query.answer("not_enought_balls")

    def selct_gift_sure(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        data = update.callback_query.data.split(":")
        if data[0] == "sure_select_gift":
            if data[1] == "yes":
                context.user_data['current_gift'].take(db_user)
                update.callback_query.message.edit_text(
                    db_user.text("accept_your_prompt"))
                return self.start(update, context, False)
            else:
                update.callback_query.message.delete()
                context.user_data['tmp_message'] = user.send_message(
                    **balls_keyboard_pagination(db_user, 1), parse_mode="HTML")
                return BALL

    # @delete_tmp_message
    def cart(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        if len(db_user.busket.items) > 0:
            update.callback_query.message.edit_text(
                **busket_keyboard(db_user, context), parse_mode="HTML")
            return CART
        else:
            update.callback_query.answer(
                db_user.text("empty_cart"), show_alert=True)
            return SELECT_CATEGORY