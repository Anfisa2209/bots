import json
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from config import BOT_TOKEN

with open('questions.json', encoding='utf8') as json_file:
    data = json.load(json_file)['questions']


async def start(update, context):
    context.user_data['answers'] = {'questions': [], 'right_answers': 0, 'wrong_answers': 0}
    context.user_data['game_on'] = False

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Да', callback_data='yes')],
                                         [InlineKeyboardButton('Нет', callback_data='no')]])

    await update.message.reply_text(
        'Знание литературы проверили, теперь проверим знание истории😊. Ответьте на 10 вопросов.',
        reply_markup=reply_markup)


async def ask_question(context, chat_id):
    user_data = context.user_data
    answers = user_data['answers']

    # Выбираем вопрос, которого ещё не было
    available_questions = [q for q in data if q['question'] not in [item[0] for item in answers['questions']]]

    if not available_questions:
        await context.bot.send_message(chat_id, "Все вопросы закончились!")
        return
    question_data = random.choice(available_questions)
    question = question_data['question']
    response = question_data['response']

    answers['questions'].append((question, response))

    await context.bot.send_message(
        chat_id,
        f'Уважаемые знатоки, внимание на экран:\nВопрос {len(answers["questions"])}: {question}'
    )


async def stop(update, context):
    context.user_data.clear()
    await update.message.reply_text('Как, уже уходите? Ну и ладно, до свидания!')


async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        await query.edit_message_text(text='Да начнется игра!')
        context.user_data['game_on'] = True
        chat_id = query.message.chat.id
        await ask_question(context, chat_id)
    elif query.data == 'no':
        await query.edit_message_text(text='Не хотите проверять знания по истории? Ну и ладно! До свидания!')


async def check_response(update, context):
    if context.user_data.get('game_on', False):
        user_answer = update.message.text
        answers = context.user_data['answers']

        current_question = answers['questions'][-1]
        right_answer = current_question[1]

        if user_answer.strip() == right_answer.strip():
            answers['right_answers'] += 1
            await update.message.reply_text('Совершенно верно!')
        else:
            answers['wrong_answers'] += 1
            await update.message.reply_text(f'Неверно! Правильный ответ: {right_answer}. Пойдемте дальше')

        if len(answers['questions']) >= 10:
            await update.message.reply_text(
                f"Игра окончена! Правильных ответов: {answers['right_answers']}, "
                f"Неправильных: {answers['wrong_answers']}"
            )
            context.user_data.clear()
        else:
            chat_id = update.message.chat.id
            await ask_question(context, chat_id)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_response))
    application.run_polling()


if __name__ == '__main__':
    main()
