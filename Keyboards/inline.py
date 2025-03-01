from aiogram.types import InlineKeyboardButton
from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder


inline_kb_router = Router()

options = {
    "Количество уровней": {
        "1 уровень": 400,
        "2 уровня": 750,
        "3 уровня": 1100,
    },
    "Форма": {
        "Квадрат": 600,
        "Круг": 400,
        "Прямоугольник": 1000,
    },
    "Топпинг": {
        "Без топпинга": 0,
        "Белый соус": 200,
        "Карамельный сироп": 180,
        "Кленовый сироп": 200,
        "Клубничный сироп": 300,
        "Черничный сироп": 350,
        "Молочный шоколад": 200,
    },
    "Ягоды": {
        "Без ягод": 0,
        "Ежевика": 400,
        "Малина": 300,
        "Голубика": 450,
        "Клубника": 500,
    },
    "Декор": {
        "Без декора":0,
        "Фисташки": 300,
        "Безе": 400,
        "Фундук": 350,
        "Пекан": 300,
        "Маршмеллоу": 200,
        "Марципан": 280,
    },
    "Надпись": {
        "Без надписи": 0,
        "Добавить надпись": 500,
    },
}

user_choices = {}


def create_keyboard(category):
    keyboard = InlineKeyboardBuilder()
    for option, price in options[category].items():
        keyboard.add(InlineKeyboardButton(text=f"{option} ({price}₽)", callback_data=f"{category}|{option}"))
    return keyboard.adjust(2)


@inline_kb_router.callback_query(lambda call: True)
async def callback_handler(call: types.CallbackQuery):
    global user_choices
    category, option = call.data.split('|')
    price = options[category][option]

    if "Выбор" not in user_choices:
        user_choices["Выбор"] = {}
    if "Цена" not in user_choices:
        user_choices["Цена"] = 0

    user_choices["Выбор"][category] = option
    user_choices["Цена"] += price

    categories = list(options.keys())
    next_index = categories.index(category) + 1

    if next_index < len(categories):
        next_category = categories[next_index]
        await call.message.edit_text(f"Выберите {next_category.lower()}:", reply_markup=create_keyboard(next_category).as_markup())
    else:
        summary = "Ваш выбор:\n" + "\n".join(f"{cat}: {opt}" for cat, opt in user_choices["Выбор"].items())
        summary += f"\nОбщая цена: {user_choices['Цена']}₽"
        await call.message.edit_text(summary)

    await call.answer()
