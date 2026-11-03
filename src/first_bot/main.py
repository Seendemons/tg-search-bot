import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from first_bot.handlers import router
from aiogram.types import BotCommand


load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']

bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher()
dispatcher.include_router(router)

async def start_bot():
    commands = [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Показать справку"),
            BotCommand(command="search", description="Начать поиск"),
        ]

    await bot.set_my_commands(commands)

    await dispatcher.start_polling(bot)

def main():
    asyncio.run(start_bot())
