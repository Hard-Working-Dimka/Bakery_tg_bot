import datetime
import requests
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
import pytz

from Common.tools import is_within_24_hours
from Common.requests_db import request_db_is_ready_cakes, request_db_to_post_order_list
from Keyboards import reply


TIME_ZONE = pytz.timezone('Europe/Moscow')
cake_router = Router()


# FSM for cake
class GetCakes(StatesGroup):
    name = State()
    phone_number = State()
    address = State()
    cake = State()
    delivery = State()


@cake_router.message(Command('cakeslist'))
@cake_router.message(StateFilter(None), F.text.contains('Заказать тортик'))
async def choose_cake(message: types.Message, state: FSMContext):
    ready_cakes = request_db_is_ready_cakes()
    keyboard_for_choose_cake = ReplyKeyboardBuilder()

    for cake in ready_cakes:
        if not cake['name'] == 'Кастомный':
            keyboard_for_choose_cake.add(KeyboardButton(text=f"{cake['name']}"))
            keyboard_for_choose_cake.adjust(1)

            await message.answer(
                text=f'''<b>Название</b>: {cake['name']}.
                    \n<b>Описание</b>: {cake['description']}.
                    \n<b>Состав</b>: {cake['ingredients']}.
                    \n<b>Цена</b>: {cake['price']}.
                    \n<b>Фото</b>: {cake['photo']}''', parse_mode=ParseMode.HTML,
                reply_markup=keyboard_for_choose_cake.as_markup(resize_keyboard=True))

    await state.set_state(GetCakes.cake)


@cake_router.message(GetCakes.cake, F.text)
async def get_user_info_cake(message: types.Message, state: FSMContext):
    await state.update_data(cake=message.text)
    await message.answer('Вы выбрали торт', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите номер телефона')
    await state.set_state(GetCakes.phone_number)


@cake_router.message(GetCakes.phone_number, F.text)
async def get_user_info_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Введите адрес')
    await state.set_state(GetCakes.address)


@cake_router.message(GetCakes.address, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите имя')
    await state.set_state(GetCakes.name)


@cake_router.message(GetCakes.name, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите дату доставки в формате ДД.ММ.ГГ ЧЧ:ММ (+20% если в течении 24 часов):')
    await state.set_state(GetCakes.delivery)


@cake_router.message(GetCakes.delivery, F.text)
async def got_offer(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    data = await state.get_data()
    date_receiving_order = datetime.datetime.strptime(data['delivery'], '%d.%m.%y %H:%M')
    total_price = float
    ready_cakes = request_db_is_ready_cakes()

    for cake in ready_cakes:
        if cake['name'] == data['cake']:
            total_price = float(cake['price'])

    if is_within_24_hours(date_receiving_order):
        total_price += total_price * 0.2

    payload_order = {
        "address": {data['address']},
        "total_price": f'{total_price}',
        "delivery": {date_receiving_order.isoformat()},
        "phone_number": {data['phone_number']},
        "created": {datetime.datetime.now().isoformat()},
        "comment": "",
        "customer": {message.from_user.id},
        "cake": {data['cake']},
        "variables_of_modifications": {},
    }

    try:

        request_db_to_post_order_list(payload_order)
        await message.answer('Заказ принят🤙', reply_markup=reply.keyboard)

    except requests.exceptions.HTTPError:
        await message.answer('Заказ не удалось принять, ошибка сервера')

    await state.clear()
