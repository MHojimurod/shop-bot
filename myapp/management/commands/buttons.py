from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def lang_btn():
    btn = [
        [InlineKeyboardButton("UZ", callback_data='UZ'), InlineKeyboardButton(
            "RU", callback_data='RU')]
    ]
    return InlineKeyboardMarkup(btn)