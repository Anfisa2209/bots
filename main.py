from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler

import random
import math

from config import BOT_TOKEN

base_keyboard = [['/dice', '/timer']]
dice_keyboard = [['/6', '/2x6', '/20', '/back']]
timer_keyboard = [['/30s', '/1m', '/5m', '/back']]
close_keyboard = [['/close']]

base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
active_timer_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text('Привет! Я бот-гадалка!')
    await update.message.reply_text("/dice: кинуть кубики, /timer: засечь время", reply_markup=base_markup)


async def dices(update, context):
    await update.message.reply_text("кинуть кубики: 6 граней, 2 по 6, 20 или вернуться назад", reply_markup=dice_markup)


async def dice6(update, context):
    number = math.trunc(random.random() * 6) + 1
    await update.message.reply_text("{0}".format(number))


async def dice2x6(update, context):
    number1 = math.trunc(random.random() * 6) + 1
    number2 = math.trunc(random.random() * 6) + 1
    await update.message.reply_text("{0} {1}".format(number1, number2))


async def dice20(update, context):
    number = math.trunc(random.random() * 20) + 1
    await update.message.reply_text("{0}".format(number))


# Управление таймерами.

async def timers(update, context):
    await update.message.reply_text("засечь: 30 сек., 1 мин., 5 мин.  или вернуться назад", reply_markup=timer_markup)


async def set_timer(update, context, delay):
    job = context.job_queue.run_once(finish_timer, delay, chat_id=update.message.chat_id, data=delay)

    context.chat_data['job'] = job
    await update.message.reply_text(f'Установлен таймер на {delay} секунд', reply_markup=active_timer_markup)


async def finish_timer(context):
    job = context.job
    await context.bot.send_message(job.chat_id, text='Время истекло.', reply_markup=timer_markup)


async def reset_timer(update, context):
    if 'job' in context.chat_data:
        context.chat_data['job'].schedule_removal()
        del context.chat_data['job']

    await update.message.reply_text('Таймер сброшен.', reply_markup=timer_markup)


# Таймеры

async def timer30s(update, context):
    await set_timer(update, context, 30)


async def timer1m(update, context):
    await set_timer(update, context, 60)


async def timer5m(update, context):
    await set_timer(update, context, 300)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Переключение режимов
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", dices))
    application.add_handler(CommandHandler("timer", timers))
    application.add_handler(CommandHandler("back", start))

    # Кубики
    application.add_handler(CommandHandler("6", dice6))
    application.add_handler(CommandHandler("2x6", dice2x6))
    application.add_handler(CommandHandler("20", dice20))

    # Таймеры
    application.add_handler(CommandHandler("30s", timer30s))
    application.add_handler(CommandHandler("1m", timer1m))
    application.add_handler(CommandHandler("5m", timer5m))
    application.add_handler(CommandHandler("close", reset_timer))

    application.run_polling()


if __name__ == '__main__':
    main()
