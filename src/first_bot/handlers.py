from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from first_bot.github import search_github
from first_bot.stackoverflow import search_stackoverflow
from first_bot.wikipedia import search_wiki

router = Router()


class SearchStates(StatesGroup):
    waiting_for_query = State()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я твой первый бот.\nНапиши /help чтобы узнать что я умею")


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

    wiki_media = await search_wiki(query)
    github_media = await search_github(query)
    stackoverflow_media = await search_stackoverflow(query)

    # Википедия:
    receive = "\n".join(wiki_media)
    await message.answer(receive)

    # Github:
    receive = "\n".join(github_media)
    await message.answer(receive)

    # StackOverflow
    receive = "\n".join(stackoverflow_media)
    await message.answer(receive)
