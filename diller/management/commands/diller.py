from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler)
from telegram import User
from .constant import (
    SELECT_CATEGORY,
    TOKEN,
    LANGUAGE,
    NAME,
    NUMBER,
    REGION,
    DISTRICT,
    MENU
)

from diller.models import Diller
from diller.stages import Register, Menu





user: User
db_user: Diller




class Bot(Updater, Register, Menu):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        not_start = ~Filters.regex("^(\/start)")

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler('start',self.start)
                ],
            states={
                LANGUAGE: [MessageHandler(Filters.regex("^(🇺🇿|🇷🇺)") & not_start, self.language)],
                NAME: [MessageHandler(Filters.text & not_start, self.name) ],
                NUMBER: [MessageHandler(Filters.contact & not_start, self.number) ],
                REGION: [MessageHandler(Filters.text & not_start, self.region) ],
                DISTRICT: [MessageHandler(Filters.text & not_start, self.district) ],
                MENU: [
                    MessageHandler(Filters.regex("^(Sotib olish|Купить)"), self.buy),
                    MessageHandler(Filters.regex("^(Sotib olingan|Купленные)"), self.purchased),
                    MessageHandler(Filters.regex("^(Mening ballarim|Мои баллы)"), self.my_balls)
                    ],
                SELECT_CATEGORY: [MessageHandler(Filters.regex("^\d+$") & not_start, self.buy), CallbackQueryHandler(self.buy, pattern="^category_pagination:"), CallbackQueryHandler(self.start, pattern="^cancel_pagination" )],
            },
            fallbacks=[
                CommandHandler('start',self.start)
            ]
        )
        self.dispatcher.add_handler(self.conversation)

        self.start_polling()
        print('polling')
        self.idle()
    

    
    
            
        
x = Bot(TOKEN)