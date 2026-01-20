import os
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ===== НАСТРОЙКИ =====

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Ошибка: переменная TOKEN не задана!")

# Админы прописаны напрямую (для bothost / free-хостингов)
ADMINS = [228986476, 1197066931]

# ===== ИНИЦИАЛИЗАЦИЯ =====

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== ОБРАБОТКА /start =====

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Здравствуйте! Напишите ваш вопрос, и администратор вам ответит.")

# ===== ОБРАБОТКА СООБЩЕНИЙ ОТ ПОЛЬЗОВАТЕЛЕЙ =====

@dp.message()
async def handle_message(message: Message):
    user = message.from_user
    user_id = user.id

    # Если админ пишет команду ответа
    if user_id in ADMINS and message.text.startswith("/reply"):
        await handle_admin_reply(message)
        return

    # Обычное сообщение пользователя → админам
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text_for_admins = (
        "📩 Новое сообщение от пользователя:\n\n"
        f"ID: {user_id}\n"
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
                    callback_data=f"reply:{user_id}"
                )
            ]
        ]
    )

    for admin in ADMINS:
        await bot.send_message(admin, text_for_admins, reply_markup=keyboard)

    await message.answer("✅ Ваше сообщение отправлено администраторам.")

# ===== CALLBACK ДЛЯ КНОПКИ =====

@dp.callback_query(lambda c: c.data.startswith("reply:"))
async def reply_button_handler(callback):
    user_id = callback.data.split(":")[1]
    await callback.message.answer(
        f"Введите команду:\n\n"
        f"/reply {user_id} текст_ответа"
    )
    await callback.answer()

# ===== ОТВЕТ АДМИНА ПОЛЬЗОВАТЕЛЮ =====

async def handle_admin_reply(message: Message):
    try:
        _, user_id, *reply_text = message.text.split()
        user_id = int(user_id)
        reply_text = " ".join(reply_text)

        if not reply_text:
            await message.answer("❌ Текст ответа пуст.")
            return

        await bot.send_message(
            user_id,
            f"💬 Ответ администратора:\n\n{reply_text}"
        )
        await message.answer("✅ Ответ отправлен пользователю.")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# ===== ЗАПУСК =====

async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
