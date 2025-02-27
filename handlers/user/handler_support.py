from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

import keyboards.user.keyboard_order as kb
from keyboards.start_keyboard import keyboard_start
import database.requests as rq
from database.models import User
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins_photo, send_message_admins_text
from config_data.config import Config, load_config

import logging
from datetime import datetime, timedelta

config: Config = load_config()
router = Router()


class OrderState(StatesGroup):
    text_order = State()
    photo_order = State()
    deadline = State()


@router.message(F.text == 'Поддержка 🧑‍💻')
@error_handler
async def press_button_order(message: Message, bot: Bot) -> None:
    """
    Запуск процедуры отправки заявки
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'press_button_order: {message.chat.id}')
    await message.answer(text=f'🌟 Добро пожаловать в службу поддержки! 🌟\n\n'
                              f'Здравствуйте! Мы рады видеть вас здесь. '
                              f'Если у вас возникли вопросы или проблемы, мы готовы помочь вам!\n\n'
                              f'По всем вопросам пишите @NikulinFedor')

