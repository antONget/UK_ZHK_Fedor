from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter

import keyboards.admin.keyboards_edit_list_personal as kb
import database.requests as rq
from database.models import User
from filter.admin_filter import IsSuperAdmin
from utils.error_handling import error_handler


import asyncio
import logging


router = Router()


class Personal(StatesGroup):
    id_tg_personal = State()


# Персонал
@router.message(F.text == 'Исполнители', IsSuperAdmin())
@error_handler
async def process_change_list_personal(message: Message, bot: Bot) -> None:
    """
    Выбор роли для редактирования списка
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'process_change_list_personal: {message.chat.id}')
    try:
        await message.edit_text(text="Выберите роль которую вы хотите изменить.",
                                reply_markup=kb.keyboard_select_role())
    except:
        await message.answer(text="Выбeрите роль которую вы хотите изменить.",
                             reply_markup=kb.keyboard_select_role())


@router.callback_query(F.data.startswith('edit_list_'))
@error_handler
async def process_select_action(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Выбор действия которое нужно совершить с ролью при редактировании
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_add_admin: {callback.message.chat.id}')
    edit_role = callback.data.split('_')[2]
    role = '<b>ИСПОЛНИТЕЛЯ</b>'
    await state.update_data(edit_role=edit_role)
    await callback.message.edit_text(text=f"Назначить или разжаловать пользователя как {role}?",
                                     reply_markup=kb.keyboard_select_action())
    await callback.answer()


@router.callback_query(F.data == 'personal_add')
@error_handler
async def process_personal_add(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Действие добавления пользователя в список выбранной роли
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_personal_add: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕМ</b>'
    await callback.message.edit_text(text=f'Пришлите id telegram пользователя для назначения его {role}.\n\n'
                                          f'Важно!!! Пользователь должен запустить бота.\n\n'
                                          f'Получить id telegram пользователя можно при помощи бота: '
                                          f'@getmyid_bot или @username_to_id_bot',
                                     reply_markup=None)
    await state.set_state(Personal.id_tg_personal)


@router.message(F.text, StateFilter(Personal.id_tg_personal))
@error_handler
async def get_id_tg_personal(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем id телеграм для добавления в список выбранной роли
    :param message:
    :param state:
    :param bot:
    :return:
    """
    if message.text in ['Исполнители', 'Рассылка', 'Отчет', 'Заявки']:
        await message.answer(text='Изменение списка ИСПОЛНИТЕЛЕЙ прервано')
        await state.set_state(state=None)
        return
    if message.text.isdigit():
        tg_id_personal = int(message.text)
    else:
        await message.answer(text='id пользователя должно состоять только из цифр, например 6632926430')
        return
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    user: User = await rq.get_user_by_id(tg_id=tg_id_personal)
    if user:
        await rq.set_user_role(tg_id=tg_id_personal, role=rq.UserRole.executor)
        await message.answer(text=f'Пользователь <a href="tg://user?id={user.tg_id}">{user.username}</a>'
                                  f' добавлен в список {role}')
        await bot.send_message(chat_id=tg_id_personal,
                               text='Вы назначены <b>ИСПОНИТЕЛЕМ</b> в проекте,'
                                    ' при необходимости перезапустите бота /start')
        await state.set_state(state=None)
    else:
        await message.answer(text=f'Пользователь c id={tg_id_personal} в базе данных не найден. '
                                  f'Для того чтобы назначить пользователя партнером он обязательно должен'
                                  f' запустить бота')
    await state.set_state(state=None)


# @router.callback_query(F.data == 'not_add_personal_list')
# @error_handler
# async def process_not_add_admin_list(callback: CallbackQuery, bot: Bot) -> None:
#     """
#     Отмена назначение пользователя партнером
#     :param callback:
#     :param bot:
#     :return:
#     """
#     logging.info(f'process_not_add_admin_list: {callback.message.chat.id}')
#     await bot.delete_message(chat_id=callback.message.chat.id,
#                              message_id=callback.message.message_id)
#     await process_change_list_personal(message=callback.message, bot=bot)
#
#
# @router.callback_query(F.data == 'add_personal_list')
# @error_handler
# async def process_add_admin_list(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
#     """
#     Подтверждение назначение партнера
#     :param callback:
#     :param state:
#     :param bot:
#     :return:
#     """
#     logging.info(f'process_add_admin_list: {callback.message.chat.id}')
#     await bot.delete_message(chat_id=callback.message.chat.id,
#                              message_id=callback.message.message_id)
#     data = await state.get_data()
#     edit_role = data['edit_role']
#     tg_id = data['add_personal']
#     role = 'партнером'
#     await rq.set_user_role(tg_id=tg_id, role=edit_role)
#     await callback.answer(text=f'Пользователь успешно назначен {role}', show_alert=True)
#     await asyncio.sleep(1)
#     await process_change_list_personal(message=callback.message, bot=bot)


@router.callback_query(F.data == 'personal_delete')
@error_handler
async def process_del_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Выбор пользователя для разжалования его из персонала
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_del_admin: {callback.message.chat.id}')
    role = 'ИСПОЛНИТЕЛЕЙ'
    list_users: list[User] = await rq.get_users_role(role=rq.UserRole.executor)
    if not list_users:
        await callback.answer(text=f'Нет пользователей для удаления из списка {role}', show_alert=True)
        return
    keyboard = kb.keyboards_del_personal(list_users=list_users,
                                         back=0,
                                         forward=2,
                                         count=6)
    await callback.message.edit_text(text=f'Выберите пользователя, которого нужно удалить из {role}',
                                     reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith('personal_del_forward'))
@error_handler
async def process_forward_del_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Пагинация по списку пользователей вперед
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_forward_del_admin: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    list_users: list[User] = await rq.get_users_role(role=rq.UserRole.executor)
    forward = int(callback.data.split('_')[-1]) + 1
    back = forward - 2
    keyboard = kb.keyboards_del_personal(list_users=list_users,
                                         back=back,
                                         forward=forward,
                                         count=6)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.edit_text(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)


@router.callback_query(F.data.startswith('personal_del_back_'))
@error_handler
async def process_back_del_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Пагинация по списку пользователей назад
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_back_del_admin: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    list_users = await rq.get_users_role(role=rq.UserRole.executor)
    back = int(callback.data.split('_')[3]) - 1
    forward = back + 2
    keyboard = kb.keyboards_del_personal(list_users=list_users,
                                         back=back,
                                         forward=forward,
                                         count=6)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.edit_text(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)


@router.callback_query(F.data.startswith('personal_del'))
@error_handler
async def process_delete_user(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Подтверждение удаления
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_delete_user: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    telegram_id = int(callback.data.split('_')[-1])
    user_info = await rq.get_user_by_id(tg_id=telegram_id)
    await state.update_data(del_personal=telegram_id)
    await callback.message.edit_text(text=f'Удалить пользователя <a href="tg://user?id={user_info.tg_id}">{user_info.username}</a> из {role}',
                                     reply_markup=kb.keyboard_del_list_personal())


@router.callback_query(F.data == 'not_del_personal_list')
@error_handler
async def process_not_del_personal_list(callback: CallbackQuery, bot: Bot) -> None:
    """
    Отмена изменения роли пользователя
    :param callback:
    :param bot:
    :return:
    """
    logging.info(f'process_not_del_personal_list: {callback.message.chat.id}')
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await callback.answer(text=f'Разжалование пользователя отменено', show_alert=True)
    await process_change_list_personal(message=callback.message, bot=bot)


@router.callback_query(F.data == 'del_personal_list')
@error_handler
async def process_del_personal_list(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_del_personal_list: {callback.message.chat.id}')
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    data = await state.get_data()
    tg_id = data['del_personal']
    role = 'ИСПОЛНИТЕЛЕЙ'
    await rq.set_user_role(tg_id=tg_id, role=rq.UserRole.user)
    await callback.answer(text=f'Пользователь успешно удален из {role}', show_alert=True)
    await asyncio.sleep(1)
    await process_change_list_personal(message=callback.message, bot=bot)
