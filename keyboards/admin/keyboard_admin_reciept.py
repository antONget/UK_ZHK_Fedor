from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import User
import logging


def keyboard_list_folder(list_folder: list, callback_prefix_select: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для вывода списка папок
    :return:
    """
    logging.info('keyboard_list_year')
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for folder in list_folder:
        buttons.append(InlineKeyboardButton(text=folder,
                                            callback_data=f'{callback_prefix_select}_{folder}'))

    kb_builder.row(*buttons, width=4)
    return kb_builder.as_markup()
