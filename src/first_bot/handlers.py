from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я твой первый бот.")


@router.message()
async def unknown_message(message: Message):
    await message.answer("Я тебя не пон")