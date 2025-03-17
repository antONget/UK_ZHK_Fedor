import os

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, PollAnswer, File
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter

from keyboards.admin.keyboard_admin_reciept import keyboard_list_folder
import database.requests as rq
from database.models import User
from filter.admin_filter import IsSuperAdmin
from utils.error_handling import error_handler
from os import listdir
from os.path import isfile, join

import asyncio
import logging


router = Router()


class Reciept(StatesGroup):
    folder_year = State()
    folder_month = State()
    add = State()


@router.message(F.text == '/квитанции', IsSuperAdmin())
@error_handler
async def add_reciept(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск процесса добавления квитанции
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_mailing: {message.chat.id}')
    path = f'{os.getcwd()}/RECIEPTS'
    await state.update_data(path=path)
    if os.listdir(path=path):
        await message.answer(text="Выберите за какой год вы добавляете квитанцию\n"
                                  "...или введите",
                             reply_markup=keyboard_list_folder(list_folder=os.listdir(path=path),
                                                               callback_prefix_select='year'))
    await state.set_state(Reciept.folder_year)


@router.message(F.text, StateFilter(Reciept.folder_year))
@error_handler
async def get_year(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем название новой папки
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_year: {message.chat.id}')
    data = await state.get_data()
    path = data['path']
    path = f'{path}/{message.text}'
    if os.path.exists(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        if not onlyfiles:
            await message.answer(text='Введите название месяца для которого хотите загрузить квитанции')
        else:
            await message.answer(text="Выберите за какой месяц вы добавляете квитанцию\n"
                                      "...или введите",
                                 reply_markup=keyboard_list_folder(list_folder=os.listdir(path=path),
                                                                   callback_prefix_select='month'))
    else:
        os.mkdir(path=path)
        await message.answer(text='Введите название месяца для которого хотите загрузить квитанции')
    await state.update_data(path=path)
    await state.set_state(Reciept.folder_month)


@router.message(F.text, StateFilter(Reciept.folder_month))
@error_handler
async def get_month(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем название новой папки
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_month: {message.chat.id}')
    data = await state.get_data()
    path = data['path']
    path = f'{path}/{message.text}'
    await state.update_data(path=path)
    await message.answer(text=f'Пришлите файл для добавления его в {message.text}')
    await state.set_state(Reciept.add)


@router.callback_query(F.data.startswith('year'))
@router.callback_query(F.data.startswith('month'))
@error_handler
async def select_period(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем выбор
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('select_period')
    period = callback.data.split('_')[0]
    select = callback.data.split('_')[-1]
    if period == 'year':
        data = await state.get_data()
        path = data['path']
        path = f'{path}/{select}'
        onlyfiles = [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]
        await state.update_data(path=path)
        await callback.message.edit_text(text="Выберите за какой месяц вы добавляете квитанцию\n"
                                              "...или введите",
                                         reply_markup=keyboard_list_folder(list_folder=onlyfiles,
                                                                           callback_prefix_select='month'))
        await state.set_state(Reciept.folder_month)
    if period == 'month':
        data = await state.get_data()
        path = data['path']
        path = f'{path}/{select}'
        await state.update_data(path=path)
        await callback.message.edit_text(text=f'Пришлите файл для добавления его в {select}')
        await state.set_state(Reciept.add)


@router.message(F.document, StateFilter(Reciept.add))
@error_handler
async def add_file(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Добавление файла
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'add_file: {message.from_user.id}')
    await state.set_state(state=None)
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # src = 'utils/new_search.pdf'
    data = await state.get_data()
    path = f'{data["path"]}.pdf'
    # Считываем содержимое из BytesIO
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    await message.answer(text="Файл с квитанциями обновлен")