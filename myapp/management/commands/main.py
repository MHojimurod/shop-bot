from telegram.ext import *
from telegram import *
from myapp.management.commands.constant import *
class Bot(Updater):
    def __init__(self, token: str = None):
        assert token, ValueError("Token is required")
        super().__init__(token)

        self.conversation = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start), CallbackQueryHandler(self.accept_request_admin, pattern="^accept_request"),
                CallbackQueryHandler(self.deny_request_admin, pattern="^deny_request"),
                CallbackQueryHandler(self.accept_request_from_user, pattern="^confirm_user_request"),
                CallbackQueryHandler(self.deny_request_from_user, pattern="^deny_user_request"),
                MessageHandler(Filters.regex("^So'rov yuborish$"), self.send_request), MessageHandler(Filters.regex("^Kutilayotgan so'rovlar"), self.get_waiting_sent_requests), MessageHandler(Filters.regex("^Tasdiqlanmagan so'rovlar"), self.unconfirmed_requests)

            ],
            states={
                NAME: [MessageHandler(Filters.text, authentication.name)],
                NUMBER: [MessageHandler(Filters.contact | Filters.regex("(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"), authentication.number), ],
                # DESCRIPTION: [MessageHandler(Filters.text, authentication.description), ],
                WAIT: [CommandHandler('start', authentication.wait_start)],
                MENU: [MessageHandler(Filters.regex("^So'rov yuborish$"), self.send_request), MessageHandler(Filters.regex("^Kutilayotgan so'rovlar"), self.get_waiting_sent_requests), MessageHandler(Filters.regex("^Tasdiqlanmagan so'rovlar"), self.unconfirmed_requests)],
                SELECT_REQUEST_TYPE: [MessageHandler(Filters.text, send_request_handler.req_type)],
                GET_TEMPLATE: [MessageHandler(Filters.text, send_request_handler.get_template_text)],
                # SELECT_CONFIRMERS: [CallbackQueryHandler(send_request_handler.add_confirmer, pattern="^add_confirmer"), CallbackQueryHandler(send_request_handler.remove_confirmer, pattern="^remove_confirmer"), CallbackQueryHandler(send_request_handler.done_request, pattern="^done_request"), CallbackQueryHandler(send_request_handler.cancel_request, pattern="^cancel_request")],
                CHECK_REQUEST_TRUE_OR_FALSE: [CallbackQueryHandler(send_request_handler.confirm_request, pattern="^temp_accept_request_true"), CallbackQueryHandler(send_request_handler.error_request, pattern="^error_request_false")],
                GET_COMMENT_FOR_REQUEST: [MessageHandler(
                    Filters.text, self.get_comment_for_request)]
            },
            fallbacks=[CommandHandler('start', self.start), CallbackQueryHandler(self.accept_request_admin, pattern="^accept_request"),
                CallbackQueryHandler(self.deny_request_admin, pattern="^deny_request"),
                CallbackQueryHandler(self.accept_request_from_user, pattern="^confirm_user_request"),
                CallbackQueryHandler(self.deny_request_from_user, pattern="^deny_user_request"),
                MessageHandler(Filters.regex("^So'rov yuborish$"), self.send_request), MessageHandler(Filters.regex("^Kutilayotgan so'rovlar"), self.get_waiting_sent_requests), MessageHandler(Filters.regex("^Tasdiqlanmagan so'rovlar"), self.unconfirmed_requests)]
        )

        self.dispatcher.add_handler(self.conversation)
        self.dispatcher.add_handler(CommandHandler('register_group', self.register_group))
        self.start_polling()
        print('polling')
        self.idle()


bot = Bot(TOKEN)