from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from admin_panel.models import DillerGifts, SellerGifts, i18n
from diller.models import Diller
from seller.management.commands.decorators import distribute
from seller.models import Seller


def balls_keyboard_pagination(seller:Seller, page:int):
    gifts = list(SellerGifts.objects.all())
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
        text += f"<b>{i + 1}. {gift.name(seller.language)}</b> → <b>{gift.ball} {i18n('ball')}</b> { '✔️' if seller.balls >= gift.ball else '✖️'} \n"
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
    text += f"\n\n<b>{i18n('balls')}</b> <b>{seller.balls} {i18n('ball')}</b>"
    return {
        "text": text,
        "reply_markup": InlineKeyboardMarkup(keyboard)
    }