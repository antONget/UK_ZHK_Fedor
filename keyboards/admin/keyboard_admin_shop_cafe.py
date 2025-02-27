from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import logging
from database.models import User


def keyboard_type_shop_cafe_user() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора типа объекта [Магазины],[Кафе]
    :return:
    """
    logging.info("keyboard_type_report")
    button_1 = InlineKeyboardButton(text=f'Магазины',
                                    callback_data=f'type_infrastructure_shop')
    button_2 = InlineKeyboardButton(text=f'Кафе',
                                    callback_data=f'type_infrastructure_cafe')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_type_shop_cafe_action() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора действия по инфраструктуре [Добавить],[Удалить]
    :return:
    """
    logging.info("keyboard_type_shop_cafe_action")
    button_1 = InlineKeyboardButton(text=f'Добавить',
                                    callback_data=f'action_infrastructure_add')
    button_2 = InlineKeyboardButton(text=f'Удалить',
                                    callback_data=f'action_infrastructure_del')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_send_order() -> InlineKeyboardMarkup:
    """
    Клавиатура [Добавить фото],[Добавить объект]
    :return:
    """
    logging.info("keyboard_type_report")
    button_1 = InlineKeyboardButton(text=f'Добавить фото',
                                    callback_data=f'shop_cafe_photo')
    button_2 = InlineKeyboardButton(text=f'Добавить объект',
                                    callback_data=f'shop_cafe_continue')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard




