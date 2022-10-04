from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from admin_panel.models import Gifts, i18n
from diller.models import Diller
from seller.management.commands.decorators import distribute
from seller.models import Seller
from django.db.models import Q

def balls_keyboard_pagination(seller:Seller, page:int):
    gifts = list(Gifts.objects.filter(~Q(amount=0),gift_type=1))
    gifts_count = len(gifts)
    gifts_per_page = 10
    gifts_pages = gifts_count // gifts_per_page + \
        1 if gifts_count % gifts_per_page != 0 else gifts_count // gifts_per_page


    gifts_page = gifts[(
        page - 1) * gifts_per_page:page * gifts_per_page]
    
    gifts_page_inline = []

    text = f"<b>Sizning ID raqamingiz: {seller.id}</b>\n<b>Natijalar {(page - 1) * gifts_per_page} - {(page * gifts_per_page) if (page * gifts_per_page) < gifts_count else gifts_count } of {gifts_count}</b>\n\n"

    for i in range(len(gifts_page)):
        gift = gifts_page[i]
        gifts_page_inline.append(
            InlineKeyboardButton(
                i + 1, callback_data=f"select_gift:{gift.id}")
        )
        text += f"<b>{i + 1}. {gift.name(seller.language)}</b> → <b>{gift.ball} {i18n('balls',seller.language)}</b> { '✔️' if seller.balls >= gift.ball else '✖️'} \n"
    keyboard = distribute(gifts_page_inline, 5)

    controls = []
    if page > 1:
        controls.append(InlineKeyboardButton(
            "⬅️", callback_data=f"gift_pagination:{page - 1}"))
    controls.append(InlineKeyboardButton(
        i18n("back_btn",seller.language), callback_data=f"back"))

    if page < gifts_pages:
        controls.append(InlineKeyboardButton(
            "➡️", callback_data=f"gift_pagination:{page + 1}"))
    keyboard.append(controls)
    text += f"\n\n <b>{seller.balls} {i18n('balls',seller.language)}</b>"
    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }