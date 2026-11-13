from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from first_bot.searches import search_github, search_stackoverflow, search_wiki

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

    wiki_results, wiki_message = await search_wiki(query)
    github_results, github_message = await search_github(query)
    stackoverflow_results, stackoverflow_message = await search_stackoverflow(query)

    # Wikipedia:
    if wiki_message:
        await message.answer(wiki_message)
    else:
        await message.answer("Wikipedia")
        for item in wiki_results:
            receive = f"{item.title}\n{item.description}\n{item.url}\n{item.source}"
            await message.answer(receive)

    # Github:
    if github_message:
        await message.answer(github_message)
    else:
        await message.answer("Github")
        for item in github_results:
            receive = f"{item.title}\n{item.description}\n{item.stars}\n{item.language}\n{item.url}\n{item.source}"
            await message.answer(receive)

    # StackOverflow
    if stackoverflow_message:
        await message.answer(stackoverflow_message)
    else:
        await message.answer("StackOverflow")
        for item in stackoverflow_results:
            receive = f"{item.title}\n{item.answ_count}\n{item.rating}\n{item.is_answered}\n{item.url}\n{item.source}"
            await message.answer(receive)
