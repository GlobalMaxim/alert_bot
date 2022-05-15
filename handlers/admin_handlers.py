from telebot import dp, bot
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from config import admin_id
from keyboards.default.menu import menu
from aiogram.dispatcher.filters import Command, Text
from db.database import count_users, count_requests

async def send_to_admin(dp):
    await bot.send_message(admin_id, 'Бот запущен', reply_markup=menu)
    await bot.set_my_commands([
        BotCommand(command='/restart', description='Перезапустить')
    ], scope=BotCommandScopeDefault())
    await bot.set_my_commands([
        BotCommand('show_users_count', 'Колличество пользователей'),
        BotCommand('show_all_requests_count', 'Всего запросов')
    ], scope=BotCommandScopeChat(chat_id=admin_id))

@dp.message_handler(commands=['show_users_count'])
async def count_user(message: Message):
    count = count_users()
    await message.answer(text=f'Всего {count} пользователей', reply_markup=menu)

@dp.message_handler(commands=['show_all_requests_count'])
async def count_user(message: Message):
    count = count_requests()
    await message.answer(text=f'Всего {count} Запросов', reply_markup=menu)