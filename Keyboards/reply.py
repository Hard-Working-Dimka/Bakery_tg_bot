from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Заказать тортик🎂'),
        KeyboardButton(text='Кастомизировать🎂')
        ],
        [
        KeyboardButton(text='Обратная связь ☎'),
        KeyboardButton(text='Способ оплаты 💵')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)
