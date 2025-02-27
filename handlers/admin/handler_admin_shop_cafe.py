from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

import database.requests as rq
from database.models import ShopCafe
from keyboards.admin import keyboard_admin_shop_cafe as kb
from utils.error_handling import error_handler

from utils.list_keyboard_select_item import utils_handler_pagination_one_card_photo_or_only_text
from config_data.config import Config, load_config
from filter.admin_filter import check_super_admin
from filter.user_filter import IsRoleAdmin
import logging


config: Config = load_config()
router = Router()


class InfrastructureState(StatesGroup):
    description = State()
    photo = State()


@router.message(F.text == 'Инфраструктура', IsRoleAdmin())
@error_handler
async def press_button_infrastructure(message: Message, bot: Bot) -> None:
    """
    Запуск процедуры отправки заявки
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'press_button_infrastructure: {message.chat.id}')
    await message.answer(text='Выберите действие для объекта инфраструктуры',
                         reply_markup=kb.keyboard_type_shop_cafe_action())


@router.callback_query(F.data.startswith('action_infrastructure_'))
@error_handler
async def get_type_infrastructure(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Инфраструктура
    :param callback: action_infrastructure_add, action_infrastructure_del
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_type_infrastructure: {callback.from_user.id}')
    action = callback.data.split('_')[-1]
    await state.update_data(action_object=action)
    if action == 'add':
        await callback.message.answer(text='Выберите тип инфраструктуры для добавления',
                                      reply_markup=kb.keyboard_type_shop_cafe_user())
    else:
        await callback.message.answer(text='Выберите тип инфраструктуры для удаления',
                                      reply_markup=kb.keyboard_type_shop_cafe_user())

@router.callback_query(F.data.startswith('type_infrastructure_'))
@error_handler
async def get_type_infrastructure(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Инфраструктура
    :param callback: type_infrastructure_shop, type_infrastructure_cafe
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_type_infrastructure: {callback.from_user.id}')
    type_object = callback.data.split('_')[-1]
    await state.update_data(type_object=type_object)
    place = 'КАФЕ'
    if type_object == 'shop':
        place = 'МАГАЗИНА'
    data = await state.get_data()
    action_object = data['action_object']
    if action_object == 'add':
        await callback.message.edit_text(text=f'Пришлите описание {place}',
                                         reply_markup=None)
        await state.set_state(InfrastructureState.description)
    else:
        data = await state.get_data()
        type_object = data['type_object']
        list_shop_cafe: list[ShopCafe] = await rq.get_infrastructures_type(type_object=type_object)
        if list_shop_cafe:
            await utils_handler_pagination_one_card_photo_or_only_text(list_items=list_shop_cafe,
                                                                       page=0,
                                                                       text_button_select='Удалить',
                                                                       callback_prefix_select='shopcafe_del',
                                                                       callback_prefix_back='shopcafe_back',
                                                                       callback_prefix_next='shopcafe_next_',
                                                                       callback=callback,
                                                                       message=None)
        else:
            await callback.message.edit_text(text='В разделе нет данных')
    await callback.answer()


@router.callback_query(F.data.startswith('shopcafe_back_'))
@router.callback_query(F.data.startswith('shopcafe_next_'))
@router.callback_query(F.data.startswith('shopcafe_del_'))
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
    page = int(callback.data.split('_')[-1])
    if callback.data.split('_')[-1] == 'del':
        await rq.del_infrastructures_id(id_=page)
        await callback.message.answer(text='Объект успешно удален')
        return
    data = await state.get_data()
    type_object = data['type_object']
    list_shop_cafe: list[ShopCafe] = await rq.get_infrastructures_type(type_object=type_object)
    if list_shop_cafe:
        await utils_handler_pagination_one_card_photo_or_only_text(list_items=list_shop_cafe,
                                                                   page=page,
                                                                   text_button_select='Удалить',
                                                                   callback_prefix_select='shopcafe_del',
                                                                   callback_prefix_back='shopcafe_back',
                                                                   callback_prefix_next='shopcafe_next_',
                                                                   callback=callback,
                                                                   message=None)


@router.message(F.text, StateFilter(InfrastructureState.description))
@router.message(F.photo, StateFilter(InfrastructureState.photo))
@error_handler
async def get_text_shop_cafe(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Добавление заведений
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_text_order: {message.chat.id}')
    if message.text:
        text_description = message.text
        await state.update_data(text_shop_cafe=text_description)
        data = await state.get_data()
        type_object = data['type_object']
        place = 'КАФЕ'
        if type_object == 'shop':
            place = 'МАГАЗИНА'
        await message.answer(text=f'Описание {place} получено. Можно добавить фото',
                             reply_markup=kb.keyboard_send_order())
    elif message.photo:
        photo_id = message.photo[-1].file_id
        await state.update_data(photo_shop_cafe=photo_id)
        data = await state.get_data()
        text_shop_cafe = data['text_shop_cafe']
        await message.answer_photo(photo=photo_id,
                                   caption=text_shop_cafe,
                                   reply_markup=kb.keyboard_send_order())


@router.callback_query(F.data.startswith('shop_cafe_'))
@error_handler
async def send_object(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Добавление объекта
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'send_object: {callback.from_user.id} ')
    answer = callback.data.split('_')[-1]
    if answer == 'photo':
        await callback.message.edit_text(text='Пришлите фото к заявке',
                                         reply_markup=None)
        await state.set_state(InfrastructureState.photo)
    elif answer == 'continue':
        await state.set_state(state=None)
        await callback.message.edit_text(text='Объект успешно добавлен',
                                         reply_markup=None)
        data = await state.get_data()
        photo_id = data['photo_shop_cafe']
        description = data['text_shop_cafe']
        type_object = data['type_object']
        infrastructure_data = {"photo": photo_id,
                               "description": description,
                               "type": type_object}
        await rq.add_infrastructure(data=infrastructure_data)
    await callback.answer()
