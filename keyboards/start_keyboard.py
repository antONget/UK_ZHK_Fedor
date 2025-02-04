from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from database.requests import UserRole
import logging


def keyboard_start(role: str) -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :param role:
    :return:
    """
    logging.info("keyboard_start")
    keyboard = ''
    if role == UserRole.user:
        button_1 = KeyboardButton(text='Личный кабинет 👤')
        button_2 = KeyboardButton(text='Подать заявку/обращение')
        button_3 = KeyboardButton(text='Поддержка 🧑‍💻')
        button_4 = KeyboardButton(text='Квитанция')
        button_5 = KeyboardButton(text='Инфраструктура')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3, button_4], [button_5]],
                                       resize_keyboard=True)
    elif role == UserRole.admin:
        button_1 = KeyboardButton(text='Исполнители')
        button_2 = KeyboardButton(text='Рассылка')
        button_3 = KeyboardButton(text='Отчет')
        button_4 = KeyboardButton(text='Заявки')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3], [button_4]],
                                       resize_keyboard=True)
    elif role == UserRole.executor:
        button_1 = KeyboardButton(text='Отчет')
        button_2 = KeyboardButton(text='Заявки')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]],
                                       resize_keyboard=True)
    return keyboard


def keyboard_send_question() -> InlineKeyboardMarkup:
    logging.info("keyboard_send_question")
    button_1 = InlineKeyboardButton(text='Задать вопрос', callback_data=f'send_question')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboard_change_role_admin() -> InlineKeyboardMarkup:
    logging.info("keyboard_change_role_admin")
    button_1 = InlineKeyboardButton(text='Изменить', callback_data=f'change_role_admin')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboard_select_role_admin() -> InlineKeyboardMarkup:
    logging.info("keyboard_select_role_admin")
    button_1 = InlineKeyboardButton(text='Администратор', callback_data=f'select_role_admin')
    button_2 = InlineKeyboardButton(text='Исполнитель', callback_data=f'select_role_partner')
    button_3 = InlineKeyboardButton(text='Пользователь', callback_data=f'select_role_user')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]])
    return keyboard
