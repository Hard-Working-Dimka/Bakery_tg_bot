from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from Common.requests_db import request_db_is_ready_cakes
from Keyboards import reply,inline
from Keyboards.inline import create_keyboard, user_choices, callback_handler

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f'Приветствую {message.from_user.first_name}! \n '
                         f'Я бот cakeStoоre, помогу Вам заказать вкусный тортик. 🎂🎂🎂',
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


#FSM
class GetCakes(StatesGroup):
    name = State()
    number = State()
    address = State()
    cake = State()
    customization = State()


@user_private_router.message(Command('cakeslist'))
@user_private_router.message(StateFilter(None),F.text.contains('Заказать тортик'))
async def choose_cake(message: types.Message, state:FSMContext):
    ready_cakes = request_db_is_ready_cakes()
    keyboard_for_choose_cake = ReplyKeyboardBuilder()
    for cake in ready_cakes:
        keyboard_for_choose_cake.add(KeyboardButton(text=f"Выбрать {cake['name']}"))
        keyboard_for_choose_cake.adjust(1)
        await message.answer(
            text=f'''<b>Название</b>: {cake['name']}.
                \n<b>Описание</b>: {cake['description']}.
                \n<b>Состав</b>: {cake['ingredients']}.
                \n<b>Цена</b>: {cake['price']}.
                \n<b>Фото</b>: {cake['photo']}''',parse_mode=ParseMode.HTML,
             reply_markup=keyboard_for_choose_cake.as_markup(resize_keyboard=True))
    await state.set_state(GetCakes.cake)


@user_private_router.message(GetCakes.cake,F.text)
async def get_user_info_cake(message: types.Message, state: FSMContext):
    await state.update_data(cake=message.text)
    await message.answer('Вы выбрали торт', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите номер телефона')
    await state.set_state(GetCakes.number)


@user_private_router.message(GetCakes.number,F.text)
async def get_user_info_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введите адрес')
    await state.set_state(GetCakes.address)


@user_private_router.message(GetCakes.address,F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите имя')
    await state.set_state(GetCakes.name)


@user_private_router.message(GetCakes.name,F.text)
async def get_user_info_customization(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Заказ принят🤙', reply_markup=reply.keyboard)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


@user_private_router.message(Command('customize'))
@user_private_router.message(F.text.contains('Кастомизировать'))
async def get_user_info_customization(message: types.Message, state: FSMContext):
    await message.answer('Кастомизируйте', reply_markup=create_keyboard("Количество уровней").as_markup())
    await state.update_data(customization=user_choices)
    await state.clear()
