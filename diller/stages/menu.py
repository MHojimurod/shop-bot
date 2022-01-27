
from telegram import (
    Update
)
from telegram.ext import (
    CallbackContext
)

from diller.management.commands.decorators import get_user

from diller.utils import category_pagination_inline
from ..management.commands.constant import SELECT_CATEGORY
class Menu:
    def buy(self, update:Update, context:CallbackContext):
        print('xxx')
        user, db_user= get_user(update)
        if update.message:
            context.user_data['buy']['pagination'] = 1
            context.user_data['tmp_message'] = user.send_message(**category_pagination_inline(db_user.language, context.user_data['buy']['pagination']))
        elif update.callback_query:
            data = update.callback_query.data.split(":")
            context.user_data['buy']['pagination'] = int(data[1])
            update.callback_query.message.edit_text(**category_pagination_inline(db_user.language, context.user_data['buy']['pagination']))
        return SELECT_CATEGORY














    
    def purchased(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        context.user_data['tmp_message'] = user.send_message("Sotib olingan")
    
    def my_balls(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        context.user_data['tmp_message'] = user.send_message("Sotib olingan")