from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, ADMINS

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Простое хранилище вопросов (для старта)
questions = {}

# Приветственное сообщение
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("❓ Задать вопрос")
    await message.answer(
        "Здравствуйте! Напишите ваш вопрос.",
        reply_markup=kb
    )

# Пользователь нажал "Задать вопрос"
@dp.message_handler(lambda m: m.text == "❓ Задать вопрос")
async def ask_question(message: types.Message):
    await message.answer("Напишите ваш вопрос одним сообщением.")

# Получение вопроса
@dp.message_handler(lambda m: m.from_user.id not in ADMINS)
async def receive_question(message: types.Message):
    q_id = len(questions) + 1
    questions[q_id] = message.from_user.id

    for admin in ADMINS:
        await bot.send_message(
            admin,
            f"❓ Новый вопрос #{q_id}\n"
            f"От: @{message.from_user.username}\n"
            f"Текст: {message.text}\n\n"
            f"Чтобы ответить, напишите: /reply_{q_id} текст_вашего_ответа"
        )

    await message.answer("Спасибо! Администратор скоро ответит.")

# Ответ админа
@dp.message_handler(lambda m: m.text.startswith("/reply_"))
async def admin_reply(message: types.Message):
    try:
        parts = message.text.split(" ", 1)
        q_id = int(parts[0].split("_")[1])
        answer = parts[1]
        user_id = questions.get(q_id)
        if user_id:
            await bot.send_message(user_id, f"💬 Ответ администрации:\n{answer}")
            await message.answer("Ответ отправлен пользователю ✅")
        else:
            await message.answer("Ошибка: пользователь не найден ❌")
    except:
        await message.answer("Неверный формат ответа. Используйте /reply_ID текст_ответа")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
