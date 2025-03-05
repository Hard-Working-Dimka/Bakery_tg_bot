from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


def create_keyboard(options):
    builder = ReplyKeyboardBuilder()
    for item, price in options.items():
        builder.add(KeyboardButton(text=f"{item} - {price}₽"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
