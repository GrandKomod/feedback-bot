import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Токен берём из переменной окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("Ошибка: переменная TOKEN не задана!")
    exit(1)

# Админ прописан напрямую
ADMINS = [228986476]  # <- сюда твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if message.text == "/start":
        await message.answer("Привет! Напиши свой вопрос, и администратор ответит.")
        return

    # Пересылаем сообщение админу
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"Сообщение от {message.from_user.id}:\n{message.text}")
        except Exception as e:
            print(f"Не удалось отправить сообщение администратору {admin}: {e}")

    await message.answer("Ваше сообщение отправлено администраторам!")

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
