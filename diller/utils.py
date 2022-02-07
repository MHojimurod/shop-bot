from click import BaseCommand
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from admin_panel.models import Category, Gifts, Product, Promotion, i18n
from diller.management.commands.decorators import distribute
from diller.models import Busket, Diller
import locale
locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')




def money(number:int, grouping:bool=True, lang=1):
    res = locale.currency(number, grouping=grouping).split(".")[0]
    return f"{res} {i18n('som', lang)}"



def category_pagination_inline(lang: int, page: int, context: CallbackContext):
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
        # text += f"{i + 1}. {category.name(lang)}\n"
        categorys_page_inline.append(
            InlineKeyboardButton(
                category.name(lang), callback_data=f"select_category:{category.id}")
        )
    keyboard = distribute(categorys_page_inline, 2)
    if len(context.user_data['current_busket'].items) > 0:
        keyboard.append([InlineKeyboardButton(
            "🛒 " + i18n('cart'), callback_data=f"cart")])

    controls = []
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"category_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton(
        "🔙", callback_data=f"cancel_pagination"),)

    if page < categorys_pages:
        controls.append(InlineKeyboardButton(
            "➡️", callback_data=f"category_pagination:{page + 1}"))
    keyboard.append(controls)

    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }


def product_pagination_inline(lang: int, page: int, product: Category, context: CallbackContext):
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
        text += f"<b>{i + 1}.</b> {product.name(lang)} <b><i>{product.diller_ball} {i18n('ball', lang)}</i></b>\n"
        products_page_inline.append(
            InlineKeyboardButton(
                i + 1, callback_data=f"select_products:{product.id}")
        )
    keyboard = distribute(products_page_inline, 5)
    controls = []
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"product_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton(
        "🔙", callback_data=f"cancel_pagination"),)
    if page < products_pages:
        controls.append(InlineKeyboardButton(
            "➡️", callback_data=f"product_pagination:{page + 1}"))
    keyboard.append(controls)

    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }


def product_count_inline(lang: int, product: Product, context: CallbackContext):
    count = context.user_data['product']['count']
    text = f"{product.name(lang)} <b><i>{product.diller_ball} {i18n('ball', lang)}</i></b>\n\n<b>{count} x {money(product.price, True, lang)[1:]} = {money(count * product.price, True, lang)[1:]}</b>"
    controls = []

    controls.append(InlineKeyboardButton(
        "-", callback_data=f"product_count:{count - 1}")) if count > 1 else None
    controls.append(InlineKeyboardButton(
        count, callback_data=f"cancel_product"))
    controls.append(InlineKeyboardButton(
        "+", callback_data=f"product_count:{count + 1}"))
    keyboard = []
    keyboard.append(controls)
    for line in distribute([InlineKeyboardButton(i, callback_data=f"product_count:{i}") for i in range(1, 10)], 3):
        keyboard.append(line)
    # add back button

    keyboard.append([InlineKeyboardButton("🔙", callback_data='back'), InlineKeyboardButton(
        f"📥 {i18n('add_to_cart')}", callback_data=f"add_to_cart")])


    return {
        "photo": open(product.image.path, 'rb'),
        "caption": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }



def busket_keyboard(user: Diller, context:CallbackContext):
    text:str = f"<b>Cart</b>\n\n"
    keyboard:list = []
    for item in user.busket.items:
        text += f"<b>{item.product.category.name(user.language)}\n    └{item.product.name(user.language)}→ {item.count} * {item.product.price} = {money(item.count * item.product.price, True, user.language)[1:]}</b>\n"
        controls = []
        if item.count > 1:
            controls.append(InlineKeyboardButton("-", callback_data=f"busket_item_count:{item.id}:{item.count - 1}"))
        for x in [InlineKeyboardButton(item.count, callback_data=f"{item.id}"), 
        InlineKeyboardButton(f"❌ {i18n('remove')}", callback_data=f"remove_busket_item:{item.id}"),
            InlineKeyboardButton("+", callback_data=f"busket_item_count:{item.id}:{item.count + 1}")]:

            controls.append(x)
        keyboard.append(controls)
    
    
    keyboard.append([InlineKeyboardButton(
        f"🛒 order", callback_data=f"order_busket")])
    keyboard.append([InlineKeyboardButton(
        f"🛒 add item", callback_data=f"continue")])
    keyboard.append([InlineKeyboardButton(
        f"🔙 back", callback_data=f"back")])

    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }



def diller_products_paginator(diller:Diller, page:int):
    print(diller.products())
    products = list(diller.products())
    products_count = len(products)
    cproducts_per_page = 10
    text = f"<b>Results {(page - 1) * cproducts_per_page} - {(page * cproducts_per_page) if (page * cproducts_per_page) < products_count else products_count } of {products_count}</b>\n\n"
    products_pages = products_count // cproducts_per_page + \
        1 if products_count % cproducts_per_page != 0 else products_count // cproducts_per_page
    print(products_pages)
    product_page = products[(
        page - 1) * cproducts_per_page:page * cproducts_per_page]
    products_page_inline = []

    for i in range(len(product_page)):
        product = product_page[i]
        text += f"<b>{product['product'].category.name(diller.language)}\n    \
└{product['product'].name(diller.language)} \
→ {product['count']} \
* {product['product'].price}\
= {money(product['count'] * product['product'].price, True, diller.language)[1:]}</b>\n"
    keyboard = distribute(products_page_inline, 5)

    controls = []

    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"product_pagination:{page - 1}"))
    if page < products_pages:
        controls.append(InlineKeyboardButton(
            "➡️", callback_data=f"product_pagination:{page + 1}"))

    keyboard.append(controls)
    # add back button to keyboard
    keyboard.append([InlineKeyboardButton("🔙", callback_data='back')])

    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }



def wait_accept_keyboard(user: Diller, user_busket: Busket):
    text = f"<b>{user.text('wait_accept')}\n\n</b>\n\n"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Qabul qildim", callback_data=f"order_accepted:{user_busket.id}")]])

    for item in user_busket.items:
        text += f"<b>{item.product.category.name(user.language)}\n    └{item.product.name(user.language)}→ {item.count} * {item.product.price} = {money(item.count * item.product.price, True, user.language)[1:]}</b>\n"

    return {
        "text": text,
        "reply_markup": keyboard
    }



def balls_keyboard_pagination(diller:Diller, page:int):
    gifts = list(Gifts.objects.filter(gift_type=0))
    gifts_count = len(gifts)
    gifts_per_page = 10
    gifts_pages = gifts_count // gifts_per_page + \
        1 if gifts_count % gifts_per_page != 0 else gifts_count // gifts_per_page


    gifts_page = gifts[(
        page - 1) * gifts_per_page:page * gifts_per_page]
    
    gifts_page_inline = []

    text = f"<b>Results {(page - 1) * gifts_per_page} - {(page * gifts_per_page) if (page * gifts_per_page) < gifts_count else gifts_count } of {gifts_count}</b>\n\n"

    for i in range(len(gifts_page)):
        gift = gifts_page[i]
        gifts_page_inline.append(
            InlineKeyboardButton(
                i + 1, callback_data=f"select_gift:{gift.id}")
        )
        text += f"<b>{i + 1}. {gift.name(diller.language)}</b> → <b>{gift.ball} {i18n('ball')}</b> { '✔️' if diller.balls >= gift.ball else '✖️'} \n"
    keyboard = distribute(gifts_page_inline, 5)

    controls = []
    print(page)
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"gift_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton(
        "🔙", callback_data=f"back"))

    if page < gifts_pages:
        controls.append(InlineKeyboardButton(
            "➡️", callback_data=f"gift_pagination:{page + 1}"))
    keyboard.append(controls)
    text += f"\n\n<b>{i18n('balls')}</b> <b>{diller.balls} {i18n('ball')}</b>"
    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }




def promotion_keyboard(user:Diller,  context:CallbackContext):
    keyboard = []
    controls = []
    promotion = context.user_data['promotion_product']
    if context.user_data['promotion_count'] > 1:
        controls.append(InlineKeyboardButton("-", callback_data=f"promotion_count:{context.user_data['promotion_count'] - 1}"))
    
    controls.append(InlineKeyboardButton(context.user_data['promotion_count'], callback_data=f"just"))
    controls.append(InlineKeyboardButton("+", callback_data=f"promotion_count:{context.user_data['promotion_count'] + 1}"))
    keyboard.append(controls)

    for line in distribute([InlineKeyboardButton(i, callback_data=f"promotion_count:{i}") for i in range(1, 10)], 3):
        keyboard.append(line)
    keyboard.append(
        [
            InlineKeyboardButton(user.text('back'), callback_data=f"back"),
            InlineKeyboardButton(user.text('buy'), callback_data=f"buy_promotion:{promotion.id}")
        ]
    )
    keyboard.append([InlineKeyboardButton("🔙", callback_data=f"back")])
    return InlineKeyboardMarkup(keyboard)

