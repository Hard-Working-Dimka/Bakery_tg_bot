import datetime
import requests
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
import pytz

from Common.tools import extract_price, is_within_24_hours
from Common.requests_db import request_db_is_ready_cakes, request_db_to_post_order_list
from Keyboards import reply
from Common.requests_db import (get_levels_cake, get_shapes_cake, get_berries_cake)
from Keyboards.reply import create_keyboard

custom_cake_router = Router()
TIME_ZONE = pytz.timezone('Europe/Moscow')


# FSM for custom cakes
class GetCustomCakes(StatesGroup):
    name = State()
    address = State()
    phone_number = State()
    levels = State()
    form = State()
    title = State()
    delivery = State()
    berry = State()
    

@custom_cake_router.message(Command('customcake'))
@custom_cake_router.message(StateFilter(None), F.text.contains('Собрать свой тортик'))
async def custom_cake(message: types.Message, state: FSMContext):
    ready_cakes = request_db_is_ready_cakes()

    for cake in ready_cakes:
        if cake['name'] == 'Кастомный':

            await message.answer(
                text='Выберите количество уровней', reply_markup=create_keyboard(get_levels_cake()))

    await state.set_state(GetCustomCakes.levels)


@custom_cake_router.message(GetCustomCakes.levels, F.text)
async def choose_levels(message: types.Message, state: FSMContext):
    await state.update_data(levels=message.text)
    await message.answer('Выберите форму', reply_markup=create_keyboard(get_shapes_cake()))
    await state.set_state(GetCustomCakes.form)


@custom_cake_router.message(GetCustomCakes.form, F.text)
async def choose_decor(message: types.Message, state: FSMContext):
    await state.update_data(form=message.text)
    await message.answer('Выберите ягоды', reply_markup=create_keyboard(get_berries_cake()))
    await state.set_state(GetCustomCakes.berry)


@custom_cake_router.message(GetCustomCakes.berry, F.text)
async def choose_decor(message: types.Message, state: FSMContext):
    await state.update_data(berry=message.text)
    await message.answer('Вы собрали свой кастомный торт.\nВведите свое имя:', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(GetCustomCakes.name)


@custom_cake_router.message(GetCustomCakes.name, F.text)
async def get_user_address_for_custom_cake(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите адрес доставки:')
    await state.set_state(GetCustomCakes.address)


@custom_cake_router.message(GetCustomCakes.address, F.text)
async def get_user_number_for_custom_cake(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите Ваш номер телефона:')
    await state.set_state(GetCustomCakes.phone_number)


@custom_cake_router.message(GetCustomCakes.phone_number, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=int(message.text))
    await message.answer('Введите дату доставки в формате ДД.ММ.ГГ ЧЧ:ММ (+20% если в течении 24 часов):')
    await state.set_state(GetCustomCakes.delivery)


@custom_cake_router.message(GetCustomCakes.delivery, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)

    data_custom = await state.get_data()
    total_price = sum(extract_price(data_custom[key]) for key in ['form', 'berry', 'levels'])
    date_receiving_order = datetime.datetime.strptime(data_custom['delivery'], '%d.%m.%y %H:%M')

    if is_within_24_hours(date_receiving_order):
        total_price += total_price * 0.2

    payload_order = {
                    "address": {data_custom['address']},
                    "total_price": {total_price},
                    "delivery": {date_receiving_order.isoformat()},
                    "phone_number": {data_custom['phone_number']},
                    "created": {datetime.datetime.now().isoformat()},
                    "comment": "",
                    "customer": {message.from_user.id},
                    "cake": {'Кастомный'},
                    "variables_of_modifications": {
                        f'{data_custom['form']}, {data_custom['berry']},{data_custom['levels']}'},
                    }

    try:

        await request_db_to_post_order_list(payload_order)
        await message.answer('Заказ принят🤙', reply_markup=reply.keyboard)

    except requests.exceptions.HTTPError:
        await message.answer('Заказ не удалось принять, ошибка сервера')

    await state.clear()