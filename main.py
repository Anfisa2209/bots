# Импортируем необходимые классы.
import datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler

from config import BOT_TOKEN

reply_keyboard = [['/start', '/help', '/time', '/date'],
                  ['/set', '/unset']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.",
                                    reply_markup=markup)


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}.",
                                    reply_markup=markup)


async def time(update, context):
    await update.message.reply_text(f"Сейчас {datetime.datetime.now().strftime('%H:%M:%S')}",
                                    reply_markup=markup)


async def date(update, context):
    await update.message.reply_text(f"Сегодня {datetime.datetime.today().strftime('%d.%m.%Y')}",
                                    reply_markup=markup)


TIMER = 5  # таймер на 5 секунд


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {TIMER}c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = f'Таймер отменен!' if job_removed else f'У вас нет активных таймеров.'
    await update.message.reply_text(text)


async def set_timer(update, context):
    global TIMER
    chat_id = update.effective_message.chat_id
    try:
        TIMER = int(context.args[0])
    except (IndexError, ValueError):
        TIMER = 5
    if TIMER < 0:
        await update.effective_message.reply_text("Так нельзя!!")
        return

    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Вернусь через {TIMER} с.!'
    if job_removed:
        text += " Старая задача удалена."
    await update.effective_message.reply_text(text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("close", close_keyboard))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
