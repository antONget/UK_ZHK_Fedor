from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

import database.requests as rq
from database.models import ShopCafe
from keyboards.user import keyboard_shop_cafe as kb
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins_photo, send_message_admins_text
from utils.list_keyboard_select_item import utils_handler_pagination_one_card_photo_or_only_text_without_select
from config_data.config import Config, load_config
from filter.admin_filter import check_super_admin
import logging
from datetime import datetime, timedelta

config: Config = load_config()
router = Router()


class InfrastructureState(StatesGroup):
    description = State()
    photo = State()


@router.message(F.text == 'Инфраструктура')
@error_handler
async def press_button_order(message: Message, bot: Bot) -> None:
    """
    Запуск процедуры отправки заявки
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'press_button_order: {message.chat.id}')
    await message.answer(text=f'Выберите раздел',
                         reply_markup=kb.keyboard_type_shop_cafe_user())


@router.callback_query(F.data.startswith('type_infrastructure_'))
@error_handler
async def get_type_infrastructure(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Инфраструктура
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_type_infrastructure: {callback.from_user.id}')
    type_object = callback.data.split('_')[-1]
    await state.update_data(type_object=type_object)
    list_shop_cafe: list[ShopCafe] = await rq.get_infrastructures_type(type_object=type_object)
    if list_shop_cafe:
        await utils_handler_pagination_one_card_photo_or_only_text_without_select(
            list_items=list_shop_cafe,
            page=0,
            callback_prefix_back='ushopcafe_back',
            callback_prefix_next='ushopcafe_next_',
            callback=callback,
            message=None)
    else:
        await callback.message.edit_text(text='В разделе нет данных')
    await callback.answer()


@router.callback_query(F.data.startswith('ushopcafe_back_'))
@router.callback_query(F.data.startswith('ushopcafe_next_'))
@error_handler
async def send_order(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Изменение данных
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_change_attribute: {callback.from_user.id} ')
    list_shop_cafe: list[ShopCafe] = await rq.get_infrastructures()
    page = int(callback.data.split('_')[-1])
    if list_shop_cafe:
        if list_shop_cafe:
            await utils_handler_pagination_one_card_photo_or_only_text_without_select(
                list_items=list_shop_cafe,
                page=page,
                callback_prefix_back='ushopcafe_back',
                callback_prefix_next='ushopcafe_next_',
                callback=callback,
                message=None)
