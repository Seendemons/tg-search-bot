from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я твой первый бот.")


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer("Я бот, созданный с использованием библиотеки aiogram.")


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я умею выполнять команды /start, /help, /about.")


@router.message(F.text.lower() == "как дела")
async def how_are_you(message: Message):
    await message.answer("Хорошо, учусь быть ботом!")


@router.message(F.text.lower() == "пока")
async def goodbye(message: Message):
    await message.answer("До встречи!")


@router.message(F.text.lower() == "привет")
async def greeting(message: Message):
    await message.answer("И тебе привет! Как дела?")


@router.message()
async def unknown_message(message: Message):
    await message.answer("Я тебя не пон")