from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN

poet = [i.strip() for i in open('poet.txt', encoding='utf8').readlines() if i.strip()]


async def start(update, context):
    context.user_data['cur_line'] = 0
    await update.message.reply_text(poet[0])


async def check_line(update, context):
    user_data = context.user_data
    cur_line = user_data.get('cur_line', 0)

    user_text = update.message.text
    correct_text = poet[cur_line + 1] if cur_line + 1 < len(poet) else ""

    if user_text == correct_text:
        user_data['cur_line'] = cur_line + 2
        if user_data['cur_line'] >= len(poet):
            await update.message.reply_text("Радость-то какая! Мы смогли! Давайте еще раз прочитаем?\nЕсли хотите повторить, нажмите /start")
        else:
            await update.message.reply_text(poet[user_data['cur_line']])
    else:
        await update.message.reply_text('Нет, не так')
        await suphler(update, context)


async def suphler(update, context):
    user_data = context.user_data
    cur_line = user_data.get('cur_line', 0)
    if cur_line + 1 < len(poet):
        right_line = poet[cur_line + 1]
        await update.message.reply_text(f'Подсказка:\n{right_line[:len(right_line) // 2]}...')


async def stop(update, context):
    context.user_data.clear()
    await update.message.reply_text('Ужас, уходите, не дочитав стих! Ну и ладно, до свидания!')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_line))
    application.run_polling()


if __name__ == '__main__':
    main()