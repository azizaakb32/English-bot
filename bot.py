import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from googletrans import Translator
from dictionary_lookup import get_definitions

translator = Translator()
API_TOKEN = "8390945018:AAFQrEzSA5u_N-nU5rM6hBC1x06AbCxbeO8"  # <-- O'zingizning tokeningizni yozing

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart() )
async def send_welcome(message: Message):
    await message.answer("Salom! Menga so‘z yoki gap yuboring:\n"
                         "- 1-2 so‘z: izohini topaman\n"
                         "- Ko‘p so‘z: tarjimasini qaytaraman")

@dp.message()
async def tarjimon_va_izoh(message: Message):
    text = message.text.strip()
    lang = translator.detect(text).lang

    if len(text.split()) > 2:
        # Tarjima rejimi
        dest = 'uz' if lang == 'en' else 'en'
        translated = translator.translate(text, dest=dest)
        await message.answer(f"🔁 Tarjima:\n<code>{translated.text}</code>")
    else:
        # So'z lug'at rejimi
        word = text if lang == 'en' else translator.translate(text, dest='en').text
        lookup = get_definitions(word)
        if lookup:
            await message.answer(f"<b>Word:</b> <code>{word}</code>\n\n<b>Definitions:</b>\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.answer_voice(lookup['audio'])
        else:
            await message.answer("❌ Bunday so'z topilmadi.")

if __name__ == '__main__':
    import asyncio
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
