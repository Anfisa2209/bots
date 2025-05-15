from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN

hols = {
    1: [
        [InlineKeyboardButton('Зал 2 - скульптуры', callback_data='go_2')],
        [InlineKeyboardButton('Выход', callback_data='button_exit')]
    ],
    2: [[InlineKeyboardButton('Зал 3 - картины', callback_data='go_3')]],
    3: [
        [InlineKeyboardButton('Зал 1 - хол', callback_data='go_1')],
        [InlineKeyboardButton('Зал 4 - буфет', callback_data='go_4')]
    ],
    4: [[InlineKeyboardButton('Зал 1 - хол', callback_data='go_1')]]
}


async def start(update, context):
    reply_markup = InlineKeyboardMarkup(hols[1])
    await update.message.reply_text(
        'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n'
        'Вы в холе (зал 1).\n'
        'Куда пойти дальше? Выбирайте:',
        reply_markup=reply_markup
    )


async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'go_2':
        await query.message.reply_text(
            'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n'
            'В этом зале вы видите скульптуры (зал 2).\n'
            'Куда пойти дальше? Выбирайте:',
            reply_markup=InlineKeyboardMarkup(hols[2])
        )
    elif query.data == 'button_exit':
        await query.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!')
    elif query.data == 'go_1':
        await query.message.reply_text(
            'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n'
            'Вы в холе (зал 1).\n'
            'Куда пойти дальше? Выбирайте:',
            reply_markup=InlineKeyboardMarkup(hols[1])
        )
    elif query.data == 'go_3':
        await query.message.reply_text(
            'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n'
            'В этом зале вы видите картины (зал 3).\n'
            'Куда пойти дальше? Выбирайте:',
            reply_markup=InlineKeyboardMarkup(hols[3])
        )
    elif query.data == 'go_4':
        await query.message.reply_text(
            'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n'
            'В этом зале можно поесть (зал 4).\n'
            'Куда пойти дальше? Выбирайте:',
            reply_markup=InlineKeyboardMarkup(hols[4])
        )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()


if __name__ == '__main__':
    main()