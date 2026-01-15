import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Получаем токен и ID админа из переменных окружения
TOKEN = os.getenv("TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS").split(",")))

# Создаем объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команд /start
@dp.message()
async def handle_start(message: Message):
    if message.text == "/start":
        await message.answer("Добрый день! Напишите свой вопрос.")
        return

    # Пересылаем сообщение админам
    for admin in ADMINS:
        await bot.send_message(admin, f"Сообщение от {message.from_user.id}:\n{message.text}")

    await message.answer("Ваше сообщение отправлено администраторам!")

# Основная функция запуска бота
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
