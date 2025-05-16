import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from translate import Translator

from config import BOT_TOKEN


async def start(update, context):
    context.user_data['language'] = ''
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Перевести на русский', callback_data='ru')],
                                         [InlineKeyboardButton('Перевести на английский', callback_data='en')]])

    await update.message.reply_text(
        'Я могу переводить слова или предложение! Выбери, на какой язык перевести:',
        reply_markup=reply_markup)


async def translate_sentences(update, context):
    user_data = context.user_data
    original_word = update.message.text
    normalized_word = normalize(original_word)
    language = user_data.get('language', 'en')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Переводить на русский', callback_data='ru')],
                                         [InlineKeyboardButton('Переводить на английский', callback_data='en')]])
    if normalized_word:
        translation = translate(original_word, language)

        await update.message.reply_text(text=translation, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=original_word, reply_markup=reply_markup)


async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'en':
        context.user_data['language'] = 'en'
        await query.message.reply_text(text='Напишите что-нибудь по-русски - и я переведу на английский')

    elif query.data == 'ru':
        context.user_data['language'] = 'ru'
        await query.message.reply_text(text='Напишите что-нибудь по-английски - и я переведу на русский')


def translate(word: str, dest):
    if len(word) > 50:
        return 'Слишком длинное предложение...'
    from_lang = 'ru' if dest == 'en' else 'en'
    translator = Translator(to_lang=dest, from_lang=from_lang)
    description = 'русский' if dest == 'ru' else "английский"
    translation = translator.translate(word)
    return f'Вот перевод "{word.capitalize()}" на {description} язык:\n{translation}'


def normalize(word):
    # удаляем знаки препинания
    return re.sub(r'[^\w\s]', '', word)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_sentences))
    application.run_polling()


if __name__ == '__main__':
    main()
