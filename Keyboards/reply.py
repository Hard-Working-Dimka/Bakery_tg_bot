from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from Common.requests_db import request_db_is_ready_cakes


keyboard_user_accepted = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Подтвердить👍'),
        KeyboardButton(text='Отклонить👎')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Пользовательское соглашение'
)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Заказать тортик🎂'),
        KeyboardButton(text='Собрать свой тортик🎂')
        ],
        [
        KeyboardButton(text='Обратная связь ☎'),
        KeyboardButton(text='Способ оплаты 💵')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)

customize_cake = request_db_is_ready_cakes()

def get_modifications_cake():
    for cake in customize_cake:
        if cake['name'] == 'Кастомный':
            return cake['modifications']


def get_levels_cake():
    levels = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Количество уровней':
            for variable in modification["variables_of_modification"]:
                levels[variable["tier"]] = variable["price"]
            return levels


def get_shapes_cake():
    shapes = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Форма':
            for variable in modification["variables_of_modification"]:
                shapes[variable["tier"]] = variable["price"]
            return shapes


def get_decor_cake():
    decor = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Декор':
            for variable in modification["variables_of_modification"]:
                decor[variable["tier"]] = variable["price"]
            return decor


def get_inscription_cake():
    inscription = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Надпись':
            for variable in modification["variables_of_modification"]:
                inscription[variable["tier"]] = variable["price"]
            return inscription


def create_keyboard(options):
    builder = ReplyKeyboardBuilder()
    for item, price in options.items():
        builder.add(KeyboardButton(text=f"{item} - {price}₽"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
