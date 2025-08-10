import aiohttp
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from geo import *


async def start(update, context):
    await update.message.reply_text('Я могу найти любое место на карте!')


async def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    user_request = update.message.text
    response = await get_response(geocoder_uri, params={
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "format": "json",
        "geocode": user_request
    })
    if response["response"]["GeoObjectCollection"]['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
        await context.bot.send_message(
            update.message.chat_id,
            text=f'Ничего не нашел... Кажется, {user_request} не существует.'
        )
    else:
        toponym = response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        ll, spn = get_ll_spn(toponym)
        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={ll},pm2rdm"
        await context.bot.send_photo(
            update.message.chat_id,
            static_api_request,
            caption=f"Нашёл: {toponym['name']}"
        )


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, geocoder))
    application.run_polling()


if __name__ == '__main__':
    main()
