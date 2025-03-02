from io import BytesIO

from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, InputFile, FSInputFile

from Common.requests_db import request_db_is_ready_cakes
from Keyboards import reply
from Keyboards.reply import (create_keyboard, get_levels_cake, get_shapes_cake, get_decor_cake)


user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f'Приветствую {message.from_user.first_name}! \n '
                         f'Чтобы начать, подтвердите пользовательское соглашение.',
                         reply_markup=reply.keyboard_user_accepted)
    input_file = FSInputFile('Handlers/Agreement.pdf')
    await message.answer_document(document=input_file)


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


# FSM for cake
class GetCakes(StatesGroup):
    name = State()
    number = State()
    address = State()
    cake = State()
    date_delivery = State()


@user_private_router.message(Command('cakeslist'))
@user_private_router.message(StateFilter(None), F.text.contains('Заказать тортик'))
async def choose_cake(message: types.Message, state: FSMContext, bot: Bot):
    ready_cakes = request_db_is_ready_cakes()
    keyboard_for_choose_cake = ReplyKeyboardBuilder()
    for cake in ready_cakes:
        if not cake['name'] == 'Кастомный':
            keyboard_for_choose_cake.add(KeyboardButton(text=f"Выбрать {cake['name']}"))
            keyboard_for_choose_cake.adjust(1)
            await message.answer(
                text=f'''<b>Название</b>: {cake['name']}.
                    \n<b>Описание</b>: {cake['description']}.
                    \n<b>Состав</b>: {cake['ingredients']}.
                    \n<b>Цена</b>: {cake['price']}.
                    \n<b>Фото</b>: {cake['photo']}''', parse_mode=ParseMode.HTML,
                reply_markup=keyboard_for_choose_cake.as_markup(resize_keyboard=True))
    await state.set_state(GetCakes.cake)


@user_private_router.message(GetCakes.cake, F.text)
async def get_user_info_cake(message: types.Message, state: FSMContext):
    await state.update_data(cake=message.text)
    await message.answer('Вы выбрали торт', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите номер телефона')
    await state.set_state(GetCakes.number)


@user_private_router.message(GetCakes.number, F.text)
async def get_user_info_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введите адрес')
    await state.set_state(GetCakes.address)


@user_private_router.message(GetCakes.address, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите имя')
    await state.set_state(GetCakes.name)


@user_private_router.message(GetCakes.name, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите дату доставки(+20% если в течении 24 часов):')
    await state.set_state(GetCustomCakes.date_delivery)


@user_private_router.message(GetCakes.date_delivery, F.text)
async def got_offer(message: types.Message, state: FSMContext):
    await state.update_data(date_delivery=message.text)
    await message.answer('Заказ принят🤙', reply_markup=reply.keyboard)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


# FSM for custom cakes
class GetCustomCakes(StatesGroup):
    name = State()
    address = State()
    number = State()
    levels = State()
    form = State()
    decor = State()
    title = State()
    date_delivery = State()


@user_private_router.message(Command('customcake'))
@user_private_router.message(StateFilter(None), F.text.contains('Собрать свой тортик'))
async def custom_cake(message: types.Message, state: FSMContext):
    ready_cakes = request_db_is_ready_cakes()
    for cake in ready_cakes:
        if cake['name'] == 'Кастомный':
            await message.answer(
                text='Выберите количество уровней', reply_markup=create_keyboard(get_levels_cake()))
    await state.set_state(GetCustomCakes.levels)


@user_private_router.message(GetCustomCakes.levels, F.text)
async def choose_levels(message: types.Message, state: FSMContext):
    await state.update_data(levels=message.text)
    await message.answer('Выберите форму', reply_markup=create_keyboard(get_shapes_cake()))
    await state.set_state(GetCustomCakes.form)


@user_private_router.message(GetCustomCakes.form, F.text)
async def choose_decor(message: types.Message, state: FSMContext):
    await state.update_data(form=message.text)
    await message.answer('Выберите декор', reply_markup=create_keyboard(get_decor_cake()))
    await state.set_state(GetCustomCakes.decor)


@user_private_router.message(GetCustomCakes.decor, F.text)
async def get_user_name_for_custom_cake(message: types.Message, state: FSMContext):
    await state.update_data(decor=message.text)
    await message.answer('Вы собрали свой кастомный торт.\nВведите свое имя:',
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(GetCustomCakes.name)


@user_private_router.message(GetCustomCakes.name, F.text)
async def get_user_address_for_custom_cake(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите адрес доставки:')
    await state.set_state(GetCustomCakes.address)


@user_private_router.message(GetCustomCakes.address, F.text)
async def get_user_number_for_custom_cake(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите Ваш номер телефона:')
    await state.set_state(GetCustomCakes.number)


@user_private_router.message(GetCustomCakes.number, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введите дату доставки(+20% если в течении 24 часов):')
    await state.set_state(GetCustomCakes.date_delivery)


@user_private_router.message(GetCustomCakes.date_delivery, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(date_delivery=message.text)
    await message.answer('Заказ принят🤙', reply_markup=reply.keyboard)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()