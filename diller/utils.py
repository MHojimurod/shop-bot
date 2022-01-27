from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from admin_panel.models import Category, Product
from diller.management.commands.decorators import distribute


def category_pagination_inline(lang: int, page: int):
    categorys = list(Category.objects.all())
    categorys_count = len(categorys)
    categorys_per_page = 10
    categorys_pages = categorys_count // categorys_per_page + \
        1 if categorys_count % categorys_per_page != 0 else categorys_count // categorys_per_page
    print(categorys_pages)
    categorys_page = categorys[(
        page - 1) * categorys_per_page:page * categorys_per_page]
    categorys_page_inline = []
    text = "Categorys\n\n"
    for i in range(len(categorys_page)):
        category = categorys_page[i]
        text += f"{i + 1}. {category.name(lang)}\n"
        categorys_page_inline.append(
            InlineKeyboardButton(i + 1, callback_data=f"select_category:{category.id}")
        )
    keyboard = distribute(categorys_page_inline, 5)
    controls = []
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"category_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton("❌", callback_data=f"cancel_pagination"),)
    if page < categorys_pages:
        controls.append(InlineKeyboardButton("➡️", callback_data=f"category_pagination:{page + 1}"))
    keyboard.append(controls)

    return {
        "text": text,  
        "reply_markup": InlineKeyboardMarkup(keyboard)
        }


def product_pagination_inline(lang: int, page: int, product:Category):
    products = list(Product.objects.filter(category=product))
    products_count = len(products)
    cproducts_per_page = 10
    products_pages = products_count // cproducts_per_page + \
        1 if products_count % cproducts_per_page != 0 else products_count // cproducts_per_page
    print(products_pages)
    product_page = products[(
        page - 1) * cproducts_per_page:page * cproducts_per_page]
    products_page_inline = []
    text = "Categorys\n\n"
    for i in range(len(product_page)):
        product = product_page[i]
        text += f"{i + 1}. {product.name(lang)}\n"
        products_page_inline.append(
            InlineKeyboardButton(i + 1, callback_data=f"select_products:{product.id}")
        )
    keyboard = distribute(products_page_inline, 5)
    controls = []
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"product_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton("❌", callback_data=f"cancel_pagination"),)
    if page < products_pages:
        controls.append(InlineKeyboardButton("➡️", callback_data=f"product_pagination:{page + 1}"))
    keyboard.append(controls)

    return {
        "text": text,  
        "reply_markup": InlineKeyboardMarkup(keyboard)
        }


def product_count_inline(lang:int, product:Product, context:CallbackContext):
    text = f"{product.name(lang)}\n\n"
    # text += f"Count: {product.count}\n"
    # text += f"Price: {product.price}\n"
    # text += f"Total: {product.total(lang)}\n"
    controls = []

    controls.append(InlineKeyboardButton("-", callback_data=f"product_count:{context.user_data['product']['count'] - 1}")) if context.user_data['product']['count'] > 1 else None
    controls.append(InlineKeyboardButton("❌", callback_data=f"cancel_product"))
    controls.append(InlineKeyboardButton("+", callback_data=f"product_count:{context.user_data['product']['count'] + 1}"))
    keyboard = []
    keyboard.append(controls)
    for line in distribute([InlineKeyboardButton(i, callback_data=f"set_product_count:{i}") for i in range(1, 10)], 3):
        keyboard.append(line)
    print(keyboard)
    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }