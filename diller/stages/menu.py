
from telegram import (
    Update
)
from telegram.ext import (
    CallbackContext
)

from diller.management.commands.decorators import delete_tmp_message, get_user
from diller.models import Busket

from diller.utils import balls_keyboard_pagination, busket_keyboard, category_pagination_inline, diller_products_paginator
from ..management.commands.constant import BALL, CART, PURCHASED, SELECT_CATEGORY
class Menu:
    @delete_tmp_message
    def buy(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.message:
            context.user_data['current_busket'] = db_user.busket
            context.user_data['buy']['pagination'] = 1
            context.user_data['tmp_message'] = user.send_message(**category_pagination_inline(db_user.language, context.user_data['buy']['pagination'], context), parse_mode="HTML")
        elif update.callback_query:
            data = update.callback_query.data.split(":")
            if data[0] == "category_pagination":
                context.user_data['buy']['pagination'] = int(data[1])
                update.callback_query.message.edit_text(**category_pagination_inline(db_user.language, context.user_data['buy']['pagination'], context))
            else:
                context.user_data['buy']['pagination'] = 1
                keyboard = category_pagination_inline(db_user.language, context.user_data['buy']['pagination'], context)
                # update.callback_query.message.delete()
                context.user_data['tmp_message'] = user.send_message(**keyboard, parse_mode="HTML")
        return SELECT_CATEGORY














    @delete_tmp_message
    def purchased(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.message:
            if len(db_user.products()) > 0:
                context.user_data['tmp_message'] = user.send_message(**diller_products_paginator(db_user,1), parse_mode="HTML")
            else:
                context.user_data['tmp_message'] = user.send_message("Sizda hech qanday buyurtma yo'q", parse_mode="HTML")
                return self.start(update, context)
        else:
            data = update.callback_query.data.split(":")
            if data[0] == "product_pagination":
                context.user_data['tmp_message'] = user.send_message(**diller_products_paginator(db_user, int(data[1])), parse_mode="HTML")
        return PURCHASED





    @delete_tmp_message
    def my_balls(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        context.user_data['tmp_message'] = user.send_message(**balls_keyboard_pagination(db_user, 1), parse_mode="HTML",)
        return BALL
    
    # @delete_tmp_message
    def cart(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)

        if len(db_user.busket.items) > 0:
            update.callback_query.message.edit_text(**busket_keyboard(db_user, context), parse_mode="HTML")
            return CART