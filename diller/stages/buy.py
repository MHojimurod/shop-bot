from turtle import up
from telegram import *
from telegram.ext import *
from admin_panel.models import Category, Product

from diller.management.commands.decorators import delete_tmp_message, get_user
from diller.utils import category_pagination_inline, product_pagination_inline, product_count_inline

from ..management.commands.constant import SELECT_CATEGORY, SELECT_PRODUCT, SELECT_PRODUCT_COUNT
class Buy:


    @delete_tmp_message
    def select_category(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.callback_query:
            if update.callback_query.data.startswith("select_category"):
                data = update.callback_query.data.split(":")
                category = Category.objects.get(id=data[1])
                context.user_data['buy']['category'] = category
                context.user_data['buy']['pagination'] = 1

                context.user_data['tmp_message'] = user.send_message(**product_pagination_inline(db_user.language, context.user_data['buy']['pagination'], category,context))
                return SELECT_PRODUCT

            elif update.callback_query.data.startswith("product_pagination"):

                data = update.callback_query.data.split(":")
                context.user_data['buy']['pagination'] = int(data[1])

                context.user_data['tmp_message'] = user.send_message(**product_pagination_inline(db_user.language, context.user_data['buy']['pagination'], context.user_data['buy']['category']))
                return SELECT_PRODUCT
            elif update.callback_query.data.startswith("select_products"):
                context.user_data['product'] = {}
                # set count of products
                data = update.callback_query.data.split(":")
                product = Product.objects.get(id=data[1])
                context.user_data['buy']['product'] = product
                context.user_data['product']['count'] = 1 if not db_user.busket.item(product) else context.user_data['current_busket'].item(product).count
                context.user_data['tmp_message'] = user.send_photo(**product_count_inline(db_user.language, product, context))
                return SELECT_PRODUCT_COUNT
    
    def product_count(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.callback_query:
            data = update.callback_query.data.split(":")
            context.user_data['product']['count'] = int(data[1])
            keyboard = product_count_inline(db_user.language, context.user_data['buy']['product'], context)
            keyboard.pop('photo')
            context.user_data['tmp_message'] = update.callback_query.message.edit_caption(**keyboard)
            return SELECT_PRODUCT_COUNT
    
    def add_to_cart(self, update:Update, context:CallbackContext):
        user, db_user= get_user(update)
        if update.callback_query:
            product = context.user_data['buy']['product']
            count = context.user_data['product']['count']
            context.user_data['current_busket'].add_product(product, count)
            context.user_data['buy']['pagination'] = 1
            context.user_data['tmp_message'] = user.send_message(**category_pagination_inline(db_user.language, context.user_data['buy']['pagination'], context))
            return SELECT_CATEGORY