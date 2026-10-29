from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я твой первый бот.")


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я умею выполнять команды /start и /help.")


@router.message()
async def unknown_message(message: Message):
    await message.answer("Я тебя не пон")