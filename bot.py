import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Токен бота берём из переменной окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("Ошибка: переменная TOKEN не задана!")
    exit(1)

# Админ прописан напрямую
ADMINS = [228986476,1197066931]  # <- сюда твой Telegram ID

# Создаем бот и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения последних сообщений пользователей (user_id: текст)
user_messages = {}

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # Команда для ответа от администратора
    if message.text.startswith("/reply"):
        if user_id not in ADMINS:
            await message.answer("❌ У вас нет прав администратора.")
            return
        try:
            # формат команды: /reply <user_id> <текст ответа>
            _, reply_id, *reply_text = message.text.split()
            reply_id = int(reply_id)
            reply_text = " ".join(reply_text)
            await bot.send_message(reply_id, f"💬 Ответ администратора: {reply_text}")
            await message.answer(f"✅ Ответ отправлен пользователю {reply_id}")
        except Exception as e:
            await message.answer(f"Ошибка при отправке: {e}")
        return

    # Если пользователь написал /start
    if message.text == "/start":
        await message.answer("Добрый день! Напишите свой вопрос.")
        return

    # Сохраняем сообщение пользователя
    user_messages[user_id] = message.text

    # Пересылаем сообщение админам
    for admin in ADMINS:
        await bot.send_message(admin, f"📩 Сообщение от {user_id}:\n{message.text}")

    # Ответ пользователю
    await message.answer("Ваше сообщение отправлено администраторам!")

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

