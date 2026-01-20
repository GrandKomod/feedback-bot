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


# =====================

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return

    user = message.from_user
    text = message.text.strip()

    # ===== ОТВЕТ АДМИНА =====
    if text.startswith("/reply"):
        if user.id not in ADMINS:
            await message.answer("❌ У вас нет прав администратора.")
            return

        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("❗ Формат:\n/reply user_id текст")
            return

        try:
            target_id = int(parts[1])
            reply_text = parts[2]

            await bot.send_message(
                target_id,
                f"💬 Ответ администратора:\n\n{reply_text}"
            )

            await message.answer("✅ Ответ отправлен")

        except Exception as e:
            await message.answer(f"⚠️ Ошибка: {e}")

        return

    # ===== /start =====
    if text == "/start":
        await message.answer(
            "👋 Добрый день!\n"
            "Напишите ваш вопрос — мы передадим его администраторам."
        )
        return

    # ===== СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ =====

    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = f"@{user.username}" if user.username else "—"

    admin_message = (
        "📩 Новое сообщение от пользователя\n\n"
        f"🆔 ID: {user.id}\n"
        f"👤 Имя: {user.full_name}\n"
        f"🔗 Username: {username}\n"
        f"⏰ Время: {time_str}\n\n"
        f"💬 Сообщение:\n{text}\n\n"
        f"✏️ Ответить:\n/reply {user.id} текст"
    )

    for admin in ADMINS:
        await bot.send_message(admin, admin_message)

    await message.answer("✅ Ваше сообщение отправлено администраторам!")

async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
