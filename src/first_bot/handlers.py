from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class SearchStates(StatesGroup):
    waiting_for_query = State()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я твой первый бот.")


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я умею выполнять команды /search")


@router.message(Command("search"))
async def search_command(message: Message, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_query)
    await message.answer("Что будем искать?")


@router.message(SearchStates.waiting_for_query, F.text)
async def receive_search_query(message: Message, state: FSMContext):
    query = message.text

    await state.clear()
    await message.answer(f"Ты ищешь: {query}")
