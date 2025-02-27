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
