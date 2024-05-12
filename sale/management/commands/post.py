from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    ExtBot,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    Filters
)
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeImageSize, DocumentAttributeVideo

# from telegram import ReplyKeyboardMarkup as ReplyKeyboardMarkupImp
from telegram import ReplyKeyboardMarkup

from sale.models import SaleSeller2
from .constant import (
    ADMIN_POST_CHECK,
    ADMIN_POST_KEYBOARD,
    ADMIN_POST_KEYBOARD_LINK,
    ADMIN_POST_KEYBOARD_NAME,
    ADMIN_POST_MEDIA,
    BACK,
    # EXCLUDE,
    MENU,
)
from enums import PostMediaTypeEnum
# from utils import ReplyKeyboardMarkup
from telethon import Button
from typing import Optional, Sequence, Tuple, Union
from sale.management.commands.decorators import get_user

from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


temps = {}


# class ReplyKeyboardMarkup(ReplyKeyboardMarkupImp):
#     def __init__(
#         self,
#         keyboard: Sequence[Sequence[str | KeyboardButton]] = [],
#         back: bool = True,
#         resize_keyboard: bool | None = True
#     ):
#         super().__init__(
#             [*keyboard,
#             #  [BACK if back else ""]
#             ],
#             resize_keyboard,

#         )


class AdminPost:
    bot: ExtBot

    def postHandlers(self):
        self.not_start = ~Filters.regex("^(/start)")

        return ConversationHandler(
            [CommandHandler('post', self.send_post)],
            {
                ADMIN_POST_MEDIA: [
                    MessageHandler(
                        Filters.video
                        | Filters.photo
                        | Filters.document
                        | Filters.video_note
                        | Filters.text & self.not_start,
                        self.send_post_media,
                    ),
                    # MessageHandler(Filters.Tetextxt([BACK]), self.start),
                ],
                # ADMIN_POST_KEYBOARD: [
                #     CallbackQueryHandler(
                #         self.admin_post_add_keyboard, pattern=r"add:\d+"
                #     ),
                #     CallbackQueryHandler(
                #         self.admin_post_check, pattern="^(send|cancel)$"
                #     ),
                # ],
                # ADMIN_POST_KEYBOARD_NAME: [
                #     MessageHandler(
                #         Filters.text & self.not_start, self.admin_post_add_keyboard_name
                #     )
                # ],
                # ADMIN_POST_KEYBOARD_LINK: [
                #     MessageHandler(
                #         Filters.regex(r"^https?://\S+"),
                #         self.admin_post_add_keyboard_link,
                #     ),
                # ],
                ADMIN_POST_CHECK: [
                    MessageHandler(Filters.text & self.not_start,
                                   self.admin_post_check),
                    CallbackQueryHandler(
                        self.admin_post_check, pattern="^(send|cancel)$"
                    ),
                    # MessageHandler(Filters.text([BACK]), self.send_post),
                ],
            },
            [CommandHandler("start", self.start)],
            map_to_parent={MENU: MENU},
        )

    def send_post(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)

        temps[user.id] = {}

        temp = temps[user.id]

        # if len(context.args) == 0 or context.args[0] is not 'wcpNbj':
        #     return

        user.send_message(
            "Post uchun media yuboring.", reply_markup=ReplyKeyboardMarkup([])
        )
        temps[user.id] = temp
        return ADMIN_POST_MEDIA

    def send_post_media(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        temp = temps[user.id]

        media_type = (
            PostMediaTypeEnum.VIDEO
            if update.message.video
            else (
                PostMediaTypeEnum.VIDEO_NOTE
                if update.message.video_note
                else (
                    PostMediaTypeEnum.PHOTO
                    if update.message.photo
                    else (
                        PostMediaTypeEnum.DOCUMENT
                        if update.message.document
                        else PostMediaTypeEnum.TEXT
                    )
                )
            )
        )

        temp['int1'] = media_type
        temp['str1'] = (
            update.message.text_html_urled
            if media_type == PostMediaTypeEnum.TEXT
            else update.message.caption_html_urled
        )

        f = (
            update.message.effective_attachment[-1]
            if update.message.photo
            else update.message.effective_attachment
        )
        if media_type == PostMediaTypeEnum.VIDEO:
            temp['int2'] = 0  # f.duration
            temp['int3'] = 0  # f.width
            temp['int4'] = 0  # f.height

        if media_type == PostMediaTypeEnum.VIDEO_NOTE:
            temp['int2'] = f.duration

        if media_type == PostMediaTypeEnum.PHOTO:
            temp['int3'] = f.width
            temp['int4'] = f.height

        try:
            fname = f.file_name
            temp['str5'] = fname
        except Exception:
            temp['str5'] = "photo.png" if update.message.photo else "video.mp4"

        temp['str2'] = f.file_id if f else ""
        temps[user.id] = temp
        # user.send_message("Iltimos postni tekshiring.")

        # user.send_message(
        #     "Keyboardni sozlang",
        #     reply_markup=InlineKeyboardMarkup(
        #         [[InlineKeyboardButton("➕", callback_data=f"add:0")]]
        #     ),
        # )

        self.send(update, context)
        temps[user.id] = temp
        return ADMIN_POST_KEYBOARD

    # def admin_post_add_keyboard(self, update: Update, context: CallbackContext):
    #     user, db_user = get_user(update)
    #     temp = temps[user.id]

    #     action, y = update.callback_query.data.split(":")

    #     temp['y'] = y
    #     temps[user.id] = temp

    #     user.send_message("Iltimos tugmaning nomini yuboring.")
    #     temps[user.id] = temp
    #     return ADMIN_POST_KEYBOARD_NAME

    # def admin_post_add_keyboard_name(
    #     self, update: Update, context: CallbackContext
    # ):
    #     user, db_user = get_user(update)
    #     temp = temps[user.id]

    #     temp['button_name'] = update.message.text
    #     temps[user.id] = temp
    #     user.send_message("Iltimos tugmaning linkini yuboring.")
    #     temps[user.id] = temp
    #     return ADMIN_POST_KEYBOARD_LINK

    def send(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        temp = temps[user.id]

        # keyboard = ReplyKeyboardMarkup([["Yuborish", "Bekor qilish"]])

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yuborish", callback_data="send"),
                    InlineKeyboardButton(
                        "Bekor qilish", callback_data="cancel"),
                ],
            ]
        )

        if temp['int1'] == PostMediaTypeEnum.TEXT:
            user.send_message(
                temp['str1'],
                parse_mode="HTML",
                reply_markup=keyboard
            )
        elif temp['int1'] == PostMediaTypeEnum.VIDEO:
            user.send_video(
                temp['str2'],
                caption=temp['str1'],
                parse_mode="HTML",
                reply_markup=keyboard
            )
        elif temp['int1'] == PostMediaTypeEnum.VIDEO_NOTE:
            user.send_video_note(
                temp['str2'],
            )
            user.send_message(
                "Tasdiqlaysizmi?2",
                parse_mode="HTML",
                reply_markup=keyboard
            )
        elif temp['int1'] == PostMediaTypeEnum.PHOTO:
            user.send_photo(
                temp['str2'],
                caption=temp['str1'],
                parse_mode="HTML",
                reply_markup=keyboard
            )
        elif temp['int1'] == PostMediaTypeEnum.DOCUMENT:
            user.send_document(
                temp['str2'],
                caption=temp['str1'],
                parse_mode="HTML",
                reply_markup=keyboard
            )

    def admin_post_check(self, update: Update, context: CallbackContext):
        user, db_user = get_user(update)
        temp = temps[user.id]

        # a = (
        #     (update.message.text == "Yuborish")
        #     if update.message.text in ["Yuborish", "Bekor qilish"]
        #     else None
        # )
        a = update.callback_query.data == "send"
        print("Sending",a)

        if not a:
            return self.send_post(update, context)
        print("AAAAAAAAAAAAAAA")

        user.send_message(
            "Habarlar yuborilmoqda.\n\nIltimos kuting biroz vaqt ketadi."
        )

        self.send_post_to_users(update, context)

        print("BBBBBBBBBBBBBBBBBB")
        temp['y'] = 0

        return self.start(update, context, False, False)

    def send_post_to_users(self, update: Update, context: CallbackContext) -> None:
        user, db_user = get_user(update)
        temp = temps[user.id]

        sent = 0
        fail = 0

        p_m = user.send_message(
            text=f"Post yuborilmoqda.\n\nYuborildi: {sent}\nYuborib bo'lmadi: {fail}\nProcess: 0%"
        )

        users = SaleSeller2.objects.all()
        file_type = temp['int1']
        file_id = temp['str2']  # This is the file ID on Telegram servers

        for i, u in enumerate(users):
            try:
                if file_type == PostMediaTypeEnum.TEXT:
                    context.bot.send_message(
                        chat_id=u.chat_id,
                        text=temp['str1'],
                        parse_mode=ParseMode.HTML,
                    )
                elif file_type in [PostMediaTypeEnum.PHOTO, PostMediaTypeEnum.DOCUMENT, PostMediaTypeEnum.VIDEO, PostMediaTypeEnum.VIDEO_NOTE]:
                    send_method = context.bot.send_document if file_type == PostMediaTypeEnum.DOCUMENT else context.bot.send_photo if file_type == PostMediaTypeEnum.PHOTO else context.bot.send_video_note if file_type == PostMediaTypeEnum.VIDEO_NOTE else context.bot.send_video
                    send_method(
                        chat_id=u.chat_id,
                        document=file_id if file_type == PostMediaTypeEnum.DOCUMENT else file_id,
                        caption=temp['str1'],
                        parse_mode=ParseMode.HTML,
                    )
                sent += 1
            except Exception as e:
                print(e)
                fail += 1

            if i % 100 == 0:
                p_m.edit_text(
                    f"Post yuborilmoqda.\n\nYuborildi: {sent}\nYuborib bo'lmadi: {fail}\n"
                    f"Process: {(sent + fail) / len(users) * 100:.2f}%"
                )

        context.bot.send_message(
            chat_id=user.chat_id,
            text="Habarlar yuborildi."
        )
