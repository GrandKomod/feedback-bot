from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio
import os

TOKEN = os.getenv(8508102904:AAFlxlKHtsRoXloIF-Cb_GSg5ig9r28FYG4)
ADMINS = list(map(int, os.getenv(228986476).split(",")))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if message.text == "/start":
        await message.answer("Добрый день! Напишите свой вопрос.")
        return

    # Пересылаем сообщение админам
    for admin in ADMINS:
        await bot.send_message(admin, f"Сообщение от {message.from_user.id}:\n{message.text}")

    await message.answer("Ваше сообщение отправлено администраторам!")

async def main():
    # Регистрируем диспетчер с ботом
    dp.startup.register(lambda _: print("Бот запущен"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
