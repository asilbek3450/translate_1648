import logging
from aiogram import Bot, Dispatcher, types, executor
from keyboards import start_kb
from googletrans import Translator

TELEGRAM_API_TOKEN = '6519341247:AAEETJBnMTztXTyObmX7wU4CKXkxPgqimhA'

bot = Bot(token=TELEGRAM_API_TOKEN, proxy='http://proxy.server:3128')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Salom tarjimon botiga xush kelibsiz! Kerakli tilni tanlang:", reply_markup=start_kb)

til = ''
@dp.callback_query_handler()
async def tilni_tanlash(call: types.CallbackQuery):
    global til
    if call.data == 'uz_ru':
        til = 'uz_ru'
        await bot.send_message(chat_id=call.from_user.id, text="Siz o'zbekchadan ruschaga tanladingiz\nNimani tarjima qilish kerak?")
    elif call.data == 'ru_uz':
        til = 'ru_uz'
        await bot.send_message(chat_id=call.from_user.id, text="Вы выбрали с русского на узбекский\nЧто переводить?")
    elif call.data == 'en_ru':
        til = 'en_ru'
        await bot.send_message(chat_id=call.from_user.id, text="You have chosen from English to Russian\nWhat to translate?")
    elif call.data == 'ru_en':
        til = 'ru_en'
        await bot.send_message(chat_id=call.from_user.id, text="Вы выбрали с русского на английский\nЧто переводить?")
    elif call.data == 'en_uz':
        til = 'en_uz'
        await bot.send_message(chat_id=call.from_user.id, text="You have chosen from English to Uzbek\nWhat to translate?")
    elif call.data == 'uz_en':
        til = 'uz_en'
        await bot.send_message(chat_id=call.from_user.id, text="Siz o'zbekchadan inglizchaga tanladingiz\nNimani tarjima qilish kerak?")
    else:
        print(til)
        await bot.send_message(chat_id=call.from_user.id, text="Tilni tanlashda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring!")
        


@dp.message_handler()
async def tarjima(message: types.Message):
    global til
    user_text = message.text
    tildan, tilga = til.split('_')[0], til.split('_')[1]
    tarjimon = Translator()  # Translator class orqali tarjimon degan obyekt yaratiladi
    translated_text = tarjimon.translate(text=user_text, dest=tilga, src=tildan)
    await message.answer(f"Siz so'ragan matn:{user_text}\n\nTarjimasi:\n{translated_text.text}")
    print(f"{message.from_user.full_name} shuni so'radi:\n\n{user_text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
