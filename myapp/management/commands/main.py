from telegram.ext import *
from telegram import *
from myapp.management.commands.constant import *


class Bot(Updater):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler('start',self.start_handler)
                ],
            states={},
            fallbacks=[]
        )

        self.dispatcher.add_handler(self.conversation)
        self.dispatcher.add_handler(CommandHandler(
            'register_group', self.register_group))
        self.start_polling()
        print('polling')
        self.idle()

    def start_handler(self, update:Update, context:CallbackContext):
        print("aaa")
bot = Bot(TOKEN)
