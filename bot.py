import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

TOKEN = "сыррррррррр"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message):
    await message.answer("Привет! Я твой первый бот 🤖")

@dp.message()
async def echo(message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())ы