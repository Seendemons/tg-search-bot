import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from first_bot.handlers import router

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']

bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher()
dispatcher.include_router(router)

async def start_bot():
    await dispatcher.start_polling(bot)

def main():
    asyncio.run(start_bot())