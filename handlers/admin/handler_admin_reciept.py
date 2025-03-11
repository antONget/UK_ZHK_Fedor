from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, PollAnswer, File
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter

import keyboards.admin.keyboards_mailing as kb
import database.requests as rq
from database.models import User
from filter.admin_filter import IsSuperAdmin
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins_text
from io import BytesIO

import asyncio
import logging


router = Router()


class Reciept(StatesGroup):
    add = State()


@router.message(F.text == '/квитанции', IsSuperAdmin())
@error_handler
async def add_reciept(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск процесса рассылки
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'process_mailing: {message.chat.id}')
    await message.answer(text="Пришлите файл для добавления")
    await state.set_state(Reciept.add)


@router.message(F.document, StateFilter(Reciept.add))
# @error_handler
async def get_reciept(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск процесса рассылки
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'process_mailing: {message.chat.id}')
    await state.set_state(state=None)
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    src = 'utils/new_search.pdf'

    # Считываем содержимое из BytesIO
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    await message.answer(text="Файл с квитанциями обновлен")