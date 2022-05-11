from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отримати карту повітряних тривог"),
        ],
        [
            KeyboardButton(text="Слава Україні!🇺🇦"),
        ]
    ],
    resize_keyboard=True
)