from database.models import User, Order, async_session
from sqlalchemy import select, or_, and_
import logging
from dataclasses import dataclass
from datetime import datetime


""" USER """


@dataclass
class UserRole:
    user = "user"
    executor = "executor"
    admin = "admin"


async def add_user(data: dict) -> None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            session.add(User(**data))
            await session.commit()


async def set_user_fullname(tg_id: int, fullname: str) -> None:
    """
    Обновление обращения к пользователю
    :param tg_id:
    :param fullname:
    :return:
    """
    logging.info('set_user_fullname')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.full_name = fullname
            await session.commit()


async def set_user_personal_account(tg_id: int, personal_account: str) -> None:
    """
    Обновление лицевого счета
    :param tg_id:
    :param personal_account:
    :return:
    """
    logging.info('set_user_personal_account')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.personal_account = personal_account
            await session.commit()


async def set_user_phone(tg_id: int, phone: str) -> None:
    """
    Обновление лицевого счета
    :param tg_id:
    :param phone:
    :return:
    """
    logging.info('set_user_phone')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.phone = phone
            await session.commit()


async def set_user_role(tg_id: int, role: str) -> None:
    """
    Обновление роли пользователя
    :param tg_id:
    :param role:
    :return:
    """
    logging.info('set_user_phone')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.role = role
            await session.commit()


async def get_user_by_id(tg_id: int) -> User:
    """
    Получение информации о пользователе по tg_id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user_by_id {tg_id}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_users_role(role: str) -> list[User]:
    """
    Получение списка пользователей с заданной ролью
    :param role:
    :return:
    """
    logging.info('get_users_role')
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.role == role))
        list_users = [user for user in users]
        return list_users


""" ORDERS """


@dataclass
class OrderStatus:
    create = "create"
    work = "work"
    cancel = "cancel"
    completed = "completed"


async def add_order(data: dict) -> int:
    """
    Добавление заявки пользователя
    :param data:
    :return:
    """
    logging.info(f'add_question')
    async with async_session() as session:
        new_question = Order(**data)
        session.add(new_question)
        await session.flush()
        id_ = new_question.id
        await session.commit()
        return id_


async def get_order_id(order_id: int) -> Order:
    """
    Получаем заявку по id
    :param order_id:
    :return:
    """
    logging.info('get_order_id')
    async with async_session() as session:
        return await session.scalar(select(Order).where(Order.id == order_id))


async def set_order_status(order_id: int, status: str) -> None:
    """
    Обновление статуса заявки
    :param order_id:
    :param status:
    :return:
    """
    logging.info('set_order_status')
    async with async_session() as session:
        question = await session.scalar(select(Order).where(Order.id == order_id))
        question.status = status
        await session.commit()
#
#
# async def set_question_partner(question_id: int, partner_tg_id: int, message_id: int) -> None:
#     """
#     Добавление партнера в список рассылки вопроса
#     :param question_id:
#     :param partner_tg_id:
#     :return:
#     """
#     logging.info('set_question_partner')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         partner_str = question.partner_list
#         if partner_str == '':
#             partner_str_ = f'{str(partner_tg_id)}!{message_id}'
#         else:
#             partner_list = partner_str.split(',')
#             partner_list.append(f'{str(partner_tg_id)}!{message_id}')
#             partner_str_ = ','.join(partner_list)
#         question.partner_list = partner_str_
#         await session.commit()
#
#

#
#
# async def set_question_completed(question_id: int, partner: int) -> None:
#     """
#     Добавление партнера в список рассылки вопроса
#     :param question_id:
#     :param partner:
#     :return:
#     """
#     logging.info('set_question_status')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         question.partner_solution = partner
#         current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
#         question.date_solution = current_date
#         await session.commit()
#
#
# async def set_question_quality(question_id: int, quality: int) -> None:
#     """
#     Обновление качества ответа
#     :param question_id:
#     :param quality:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         question.quality = quality
#         await session.commit()
#
#
# async def set_question_data_solution(question_id: int, data_solution: str) -> None:
#     """
#     Обновление качества ответа
#     :param question_id:
#     :param data_solution:
#     :return:
#     """
#     logging.info(f'set_question_data_solution {question_id} {data_solution}')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         question.date_solution = data_solution
#         await session.commit()
#
#
# async def set_question_comment(question_id: int, comment: str) -> None:
#     """
#     Обновление комментария к вопросу
#     :param question_id:
#     :param comment:
#     :return:
#     """
#     logging.info('set_question_comment')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         question.comment = comment
#         await session.commit()
#
#
# async def set_question_executor(question_id: int, executor: int) -> None:
#     """
#     Добавление партнера в список рассылки вопроса
#     :param question_id:
#     :param executor:
#     :return:
#     """
#     logging.info('set_question_status')
#     async with async_session() as session:
#         question = await session.scalar(select(Question).where(Question.id == question_id))
#         question.partner_solution = executor
#         await session.commit()
#
#

#
#
# async def get_question_tg_id(partner_solution: int) -> list[Question]:
#     """
#     Получаем вопрос по его id
#     :param partner_solution:
#     :return:
#     """
#     logging.info('get_question_id')
#     async with async_session() as session:
#         return await session.scalars(select(Question).where(Question.partner_solution == partner_solution))
#
#
# async def get_questions() -> list[Question]:
#     """
#     Получаем вопрос по его id
#     :return:
#     """
#     logging.info('get_question_id')
#     async with async_session() as session:
#         return await session.scalars(select(Question))
#
# """ EXECUTOR """
#
#
# async def add_executor(data: dict) -> None:
#     """
#     Добавление исполнителя в рассылку
#     :param data:
#     :return:
#     """
#     logging.info(f'add_question')
#     async with async_session() as session:
#         new_executor = Executor(**data)
#         session.add(new_executor)
#         await session.commit()
#
#
# async def set_cost_executor(question_id: int, tg_id: int, cost: int) -> None:
#     """
#     Обновление стоимости выполнения заявки партнером
#     :param question_id:
#     :param tg_id:
#     :param cost:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         executor = await session.scalar(select(Executor).where(Executor.id_question == question_id,
#                                                                Executor.tg_id == tg_id))
#         if executor:
#             executor.cost = cost
#             await session.commit()
#
#
# async def set_message_id_cost_executor(question_id: int, tg_id: int, message_id_cost: int) -> None:
#     """
#     Обновление номера сообщения с предложением стоимости решения
#     :param question_id:
#     :param tg_id:
#     :param message_id_cost:
#     :return:
#     """
#     logging.info('set_message_id_cost_executor')
#     async with async_session() as session:
#         executor = await session.scalar(select(Executor).where(Executor.id_question == question_id,
#                                                                Executor.tg_id == tg_id))
#         if executor:
#             executor.message_id_cost = message_id_cost
#             await session.commit()
#
#
# async def set_message_id_executor(question_id: int, tg_id: int, message_id: int) -> None:
#     """
#     Обновление сообщения с вопросом отправленное пользователю
#     :param question_id:
#     :param tg_id:
#     :param message_id:
#     :return:
#     """
#     logging.info('set_message_id_executor')
#     async with async_session() as session:
#         executor = await session.scalar(select(Executor).where(Executor.id_question == question_id,
#                                                                Executor.tg_id == tg_id))
#         if executor:
#             executor.message_id = message_id
#             await session.commit()
#
#
# async def get_executor(question_id: int, tg_id: int) -> Executor:
#     """
#     Получаем исполнителя по номеру рассылки вопроса
#     :param question_id:
#     :param tg_id:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         return await session.scalar(select(Executor).where(Executor.id_question == question_id,
#                                                            Executor.tg_id == tg_id))
#
#
# async def get_executor_not(question_id: int, tg_id: int) -> list[Executor]:
#     """
#     Получаем исполнителей которых не выбрали для решения вопроса
#     :param question_id:
#     :param tg_id:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         return await session.scalars(select(Executor).where(Executor.id_question == question_id,
#                                                             Executor.tg_id != tg_id))
#
#
# async def get_executors(question_id: int) -> list[Executor]:
#     """
#     Получаем исполнителей которым отправлен вопрос
#     :param question_id:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         return await session.scalars(select(Executor).where(Executor.id_question == question_id))
#
#
# async def del_executor(question_id: int, tg_id: int) -> None:
#     """
#     Удаляем всех пользователей из списка рассылки вопроса
#     :param question_id:
#     :param tg_id:
#     :return:
#     """
#     logging.info('set_question_quality')
#     async with async_session() as session:
#         executor = await session.scalar(select(Executor).where(Executor.id_question == question_id,
#                                                                Executor.tg_id == tg_id))
#         if executor:
#             await session.delete(executor)
#             await session.commit()
#
#
# """ DIALOG """
#
#
# @dataclass
# class StatusDialog:
#     active = 'active'
#     completed = 'completed'
#
#
# async def add_dialog(data: dict) -> None:
#     """
#     Добавление нового диалога между пользователем и партнером для обсуждения вопроса
#     :param data:
#     :return:
#     """
#     logging.info(f'add_dialog')
#     async with async_session() as session:
#         new_dialog = Dialog(**data)
#         session.add(new_dialog)
#         await session.commit()
#
#
# async def get_dialog_active_tg_id(tg_id: int) -> Dialog:
#     """
#     Получаем активный диалог пользователя
#     :param tg_id:
#     :return:
#     """
#     logging.info('get_dialog_active_tg_id')
#     async with async_session() as session:
#         return await session.scalar(select(Dialog).filter(and_(or_(Dialog.tg_id_user == tg_id,
#                                                                    Dialog.tg_id_partner == tg_id),
#                                                           Dialog.status == StatusDialog.active)))
#
#
# async def set_dialog_completed_tg_id(tg_id: int) -> None:
#     """
#     Закрываем диалог
#     :param tg_id:
#     :return:
#     """
#     logging.info('set_dialog_completed_tg_id')
#     async with async_session() as session:
#         dialog = await session.scalar(select(Dialog).filter(and_(or_(Dialog.tg_id_user == tg_id,
#                                                                      Dialog.tg_id_partner == tg_id),
#                                                             Dialog.status == StatusDialog.active)))
#         if dialog:
#             dialog.status = StatusDialog.completed
#             await session.commit()
