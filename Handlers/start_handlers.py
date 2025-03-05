import requests
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove, FSInputFile

from Common.requests_db import request_db_to_post_users_data
from Keyboards import reply
from Keyboards.reply import keyboard_user_accepted


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):

    payload_users_data = {
        "username": f'{message.from_user.first_name}',
        "telegram_id": message.from_user.id,
        "telegram_username": f'{message.from_user.username}'
    }

    try:

        request_db_to_post_users_data(payload_users_data)
        input_file = FSInputFile('Handlers/Agreement.pdf')
        await message.answer(text='Подтвердите пользовательское соглашение.')
        await message.answer_document(document=input_file, reply_markup=keyboard_user_accepted)

    except requests.exceptions.HTTPError:

        await message.answer(f'Приветствую {message.from_user.first_name}!', reply_markup=reply.keyboard)


@user_private_router.message(F.text.contains('Отклонить'))
async def user_accepted(message: types.Message):
    await message.answer('Пока-пока ✌', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


@user_private_router.message(F.text.contains('Подтвердить'))
async def user_accepted(message: types.Message):
    await message.answer('Я бот cakeStoоre, помогу Вам заказать вкусный тортик. 🎂🎂🎂',
                         reply_markup=reply.keyboard)


@user_private_router.message(Command('feedback'))
@user_private_router.message(F.text.contains('Обратная связь'))
async def cmd_cake_list(message: types.Message):
    await message.answer(
        '''Для отзывов по работе сервиса и получению информации о времени доставки можно обратиться:
            <b>Телефон</b> : +7123456789
            <b>TG</b> : @dunyakhin 
            <b>Email</b> : support@gmail.com''',
        parse_mode=ParseMode.HTML
                        )


@user_private_router.message(Command('payment'))
@user_private_router.message(F.text.contains('Способ оплаты'))
async def payment(message: types.Message):
    await message.answer('''Какой-то способ''')
