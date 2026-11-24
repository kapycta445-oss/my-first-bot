import asyncio
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "сырррр"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Бот запоминает, на каком шаге каждый пользователь
user_state = {}

def is_valid_phone(text: str) -> bool:
    digits = re.sub(r"\D", "", text)  # убираем всё, кроме цифр
    return len(digits) >= 10          # в телефоне минимум 10 цифр

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_state.pop(message.from_user.id, None)  # сбрасываем старый диалог
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Оставить заявку", callback_data="order")]
    ])
    await message.answer("Привет! Нажми кнопку, чтобы оставить заявку:", reply_markup=keyboard)

@dp.callback_query(F.data == "order")
async def order_start(callback: CallbackQuery):
    user_state[callback.from_user.id] = {"step": "name"}
    await callback.message.answer("Как тебя зовут?")
    await callback.answer()

@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_state and user_state[user_id]["step"] == "phone":
        user_state[user_id]["step"] = "name"
        await callback.message.answer("Ок, вернулись назад. Как тебя зовут?")
    await callback.answer()

@dp.message()
async def handle_messages(message: Message):
    user_id = message.from_user.id

    if message.text and message.text.startswith("/"):
        return

    if user_id not in user_state:
        await message.answer("Нажми /start, чтобы начать")
        return

    step = user_state[user_id]["step"]

    if step == "name":
        user_state[user_id]["name"] = message.text
        user_state[user_id]["step"] = "phone"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ])
        await message.answer("Напиши свой телефон:", reply_markup=keyboard)
    elif step == "phone":
        if not is_valid_phone(message.text):
            await message.answer("Это не похоже на телефон 🤔 Попробуй ещё раз, например: +79001234567")
            return
        user_state[user_id]["phone"] = message.text
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(f"{user_state[user_id]['name']} — {user_state[user_id]['phone']}\n")
        await message.answer("✅ Заявка принята! Мы скоро свяжемся с тобой.")
        del user_state[user_id]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())