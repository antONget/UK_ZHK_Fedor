from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from keyboards.user.keyboard_reciept import keyboard_list_folder
import database.requests as rq
from database.models import User
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins_photo, send_message_admins_text
from config_data.config import Config, load_config
from utils.search_account import search_receipt
import os
from os import listdir
from os.path import isfile, join
import logging
from datetime import datetime, timedelta

config: Config = load_config()
router = Router()


class ReceiptState(StatesGroup):
    receipt = State()


@router.message(F.text == 'Квитанция')
@error_handler
async def press_button_receipt(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск процедуры
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'press_button_receipt: {message.chat.id}')
    path = f'{os.getcwd()}/RECIEPTS'
    await state.update_data(path=path)
    if os.listdir(path=path):
        await message.answer(text="Выберите за какой год требуется квитанция",
                             reply_markup=keyboard_list_folder(list_folder=os.listdir(path=path),
                                                               callback_prefix_select='useryear'))
    else:
        await message.answer(text='Квитанции еще не загружены')


@router.callback_query(F.data.startswith('useryear'))
@router.callback_query(F.data.startswith('usermonth'))
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
    if period == 'useryear':
        data = await state.get_data()
        path = data['path']
        path = f'{path}/{select}'
        onlyfiles = [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]
        if onlyfiles:
            await state.update_data(path=path)
            await callback.message.edit_text(text="Выберите за какой месяц хотели бы получить квитанцию",
                                             reply_markup=keyboard_list_folder(list_folder=onlyfiles,
                                                                               callback_prefix_select='usermonth'))
        else:
            await callback.message.answer(text='Нет квитанций за выбранный месяц')
    if period == 'usermonth':
        data = await state.get_data()
        path = data['path']
        path = f'{path}/{select}'
        await state.update_data(path=path)
        info_user: User = await rq.get_user_by_id(tg_id=callback.from_user.id)
        answer: bool = await search_receipt(receipt=info_user.personal_account,
                                            personal_account=info_user.personal_account)
        await callback.message.delete()
        if answer:
            await callback.message.answer_document(document=FSInputFile(f'receipt/{info_user.personal_account}.pdf'))
        else:
            await callback.message.answer(text=f'Квитанция для лицевого счета {info_user.personal_account} не найдена')
    # await message.answer(text=f'Пришлите номер вашего лицевого, например <code>7811722454330</code>')


# @router.message(F.text, StateFilter(ReceiptState.receipt))
# @error_handler
# async def get_receipt(message: Message, state: FSMContext, bot: Bot):
#     """
#     Получаем номер лицевого счета пользователя
#     :param message:
#     :param state:
#     :param bot:
#     :return:
#     """
#     logging.info(f'get_receipt: {message.chat.id}')
#     receipt_user = message.text
#     if receipt_user.isdigit():
#         await search_receipt(receipt=receipt_user, tg_id=message.from_user.id)
#         await bot.send_document(chat_id=config.tg_bot.support_id,
#                                 document=FSInputFile(f'utils/{message.from_user.id}_subset.pdf'))
#     else:
#         await message.answer(text='Лицевой счет введен некорректно')


