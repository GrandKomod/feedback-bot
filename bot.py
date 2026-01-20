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


# ====================

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return

    user = message.from_user
    text = message.text.strip()

    # ===== КОМАНДА ОТВЕТА АДМИНА =====
    if text.startswith("/reply"):
        if user.id not in ADMINS:
            await message.answer("❌ У вас нет прав администратора.")
            return

        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("❗ Формат:\n/reply user_id текст")
            return

        try:
            reply_id = int(parts[1])
            reply_text = parts[2]

            await bot.send_message(
                reply_id,
                f"💬 Ответ администратора:\n\n{reply_text}"
            )

            await message.answer(f"✅ Ответ отправлен пользователю {reply_id}")

        except Exception as e:
            await message.answer(f"⚠️ Ошибка: {e}")

        return

    # ===== /start =====
    if text == "/start":
        await message.answer(
            "👋 Добрый день!\n"
            "Напишите свой вопрос."
        )
        return

    # ===== ОБЫЧНОЕ СООБЩЕНИЕ =====

    username = f"@{user.username}" if user.username else "—"
    full_name = user.full_name
    user_id = user.id
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    admin_text = (
        "📩 Новое сообщение от пользователя:\n\n"
        f"🆔 ID: {user_id}\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"⏰ Время: {time_str}\n\n"
        f"💬 Сообщение:\n{text}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Ответить пользователю",
                    callback_data=f"reply_{user_id}"
                )
            ]
        ]
    )

    for admin in ADMINS:
        await bot.send_message(
            admin,
            admin_text,
            reply_markup=keyboard
        )

    await message.answer("✅ Ваше сообщение отправлено администраторам!")

# ===== ОБРАБОТКА КНОПКИ =====
@dp.callback_query(lambda c: c.data.startswith("reply_"))
async def reply_button(callback):
    user_id = callback.data.replace("reply_", "")
    await callback.message.answer(
        f"✏️ Чтобы ответить пользователю, отправь команду:\n\n"
        f"/reply {user_id} текст_ответа"
    )
    await callback.answer()

async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

