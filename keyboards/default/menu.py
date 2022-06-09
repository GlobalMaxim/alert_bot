from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗺Отримати карту повітряних тривог"),
        ],
        [
            KeyboardButton(text="📢Увімкнути повідомлення про тривогу"),
        ]
    ],
    resize_keyboard=True
)

menu_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗺Отримати карту повітряних тривог"),
        ],
        [
            KeyboardButton(text="❌Вимкнути сповіщення про тривогу"),
        ]
    ],
    resize_keyboard=True
)