import os
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import Command

# ===== НАСТРОЙКИ =====

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Ошибка: переменная TOKEN не задана!")

ADMINS = [228986476, 1197066931]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== /start =====

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Здравствуйте!\n"
        "Напишите ваш вопрос."
    )

# ===== АДМИН: ОТВЕТ =====

@dp.message(Command("reply"))
async def admin_reply(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ У вас нет прав.")
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Использование:\n/reply user_id текст")
        return

    user_id = int(parts[1])
    reply_text = parts[2]

    await bot.send_message(
        user_id,
        f"💬 Ответ администратора:\n\n{reply_text}"
    )
    await message.answer("✅ Ответ отправлен.")

# ===== CALLBACK-КНОПКА =====

@dp.callback_query()
async def callback_handler(call: CallbackQuery):
    if not call.data.startswith("reply:"):
        return

    user_id = call.data.split(":")[1]
    await call.message.answer(
        f"Введите команду:\n\n/reply {user_id} текст_ответа"
    )
    await call.answer()

# ===== СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЕЙ =====

@dp.message()
async def user_message(message: Message):
    user = message.from_user
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = (
        "📩 Новое сообщение от пользователя:\n\n"
        f"ID: {user.id}\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"Время: {time_str}\n\n"
        f"Сообщение:\n{message.text}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Ответить пользователю",
                    callback_data=f"reply:{user.id}"
                )
            ]
        ]
    )

    for admin in ADMINS:
        await bot.send_message(admin, text, reply_markup=keyboard)

    # 🔥 ВАЖНО: ответ пользователю
    await message.answer(
        "✅ Сообщение получено.\n"
        "Мы скоро вам ответим."
    )

# ===== ЗАПУСК =====

async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
