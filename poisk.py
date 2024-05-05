from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

chat_room = {}

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуй! Запусти поиск собеседника командой /poisk")

def start_search(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    chat_room[chat_id] = None
    update.message.reply_text("Поиск начат. Подождите, когда найдется собеседник.")

def end_conversation(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in chat_room:
        partner_id = chat_room[chat_id]
        if partner_id is not None:
            del chat_room[partner_id]
            context.bot.send_message(partner_id, "Ваш собеседник завершил диалог.")
        del chat_room[chat_id]
        update.message.reply_text("Диалог завершен. Для начала нового диалога воспользуйтесь командой /poisk")

def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in chat_room and chat_room[chat_id] is not None:
        partner_id = chat_room[chat_id]
        context.bot.send_message(partner_id, update.message.text)

def match_users(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    chat_room[chat_id] = None
    for id, partner_id in chat_room.items():
        if partner_id is None:
            chat_room[chat_id] = id
            chat_room[id] = chat_id
            update.message.reply_text("Собеседник найден. Теперь вы можете начать общение.")
            context.bot.send_message(id, "Собеседник найден. Теперь вы можете начать общение.")
            break

def main() -> None:
    updater = Updater("6872026786:AAGGyLKbgvD2nr_xwzguOSFv3KOn_JHoUmo")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("poisk", match_users))
    dispatcher.add_handler(CommandHandler("zavershit", end_conversation))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()