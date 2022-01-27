from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from admin_panel.models import Category
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
            InlineKeyboardButton(i + 1, callback_data=f"category:{category.id}")
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