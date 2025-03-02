from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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


levels = {
    "1 уровень": 400,
    "2 уровня": 750,
    "3 уровня": 1100,
}

shapes = {
    "Квадрат": 600,
    "Круг": 400,
    "Прямоугольник": 1000,
}

toppings = {
    "Без топпинга": 0,
    "Белый соус": 200,
    "Карамельный сироп": 180,
    "Кленовый сироп": 200,
    "Клубничный сироп": 300,
    "Черничный сироп": 350,
    "Молочный шоколад": 200,
}

berries = {
    "Без ягод": 0,
    "Ежевика": 400,
    "Малина": 300,
    "Голубика": 450,
    "Клубника": 500,
}

decor = {
    "Без декора": 0,
    "Фисташки": 300,
    "Безе": 400,
    "Фундук": 350,
    "Пекан": 300,
    "Маршмеллоу": 200,
    "Марципан": 280,
}

inscription = {
    "Без надписи": 0,
    "Добавить надпись": 500,
}


def create_keyboard(options):
    builder = ReplyKeyboardBuilder()
    for item, price in options.items():
        builder.add(KeyboardButton(text=f"{item} - {price}₽"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
