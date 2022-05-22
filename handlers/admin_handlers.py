import asyncio
import imp
from telebot import dp, bot
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from config import admin_id
from keyboards.default.menu import menu
from aiogram.dispatcher.filters import Command, Text
from db.database import Database
from telegram_redis.redisPreparation import Redis_Preparation 
from crone.crone import scheduler


async def send_to_admin(dp):
    asyncio.create_task(scheduler(bot))
    import middlewares
    middlewares.setup(dp)
    await bot.send_message(admin_id, 'Бот запущен', reply_markup=menu)
    await bot.set_my_commands([
        BotCommand(command='/restart', description='Перезапустить')
    ], scope=BotCommandScopeDefault())
    await bot.set_my_commands([
        BotCommand('show_all_data', 'Показать статистику'),
        BotCommand('save', 'Сохранить данные')
        # BotCommand('delete', 'Очистить кеш')
        # BotCommand('show_users_count', 'Колличество пользователей'),
        # BotCommand('show_all_requests_count', 'Всего запросов')
        
        # BotCommand('append', 'ОБновить пользователей')
    ], scope=BotCommandScopeChat(chat_id=admin_id))

@dp.message_handler(commands=['show_users_count'])
async def count_user(message: Message):
    db = Database()
    count = db.count_users()
    db.close_connection()
    await message.answer(text=f'Всего {count} пользователей')

@dp.message_handler(commands=['save'])
async def save(message: Message):
    db = Database()
    values = db.save_data_to_db()
    db.close_connection()
    await message.answer(f'Добавлено {values[0]} новых пользоватеелей и обновлено {values[1]} пользователя')

@dp.message_handler(commands=['delete'])
async def reset(message: Message):
    db = Database()
    db.clear_redis()
    db.close_connection()
    await message.answer('Redis cleared')


@dp.message_handler(commands=['show_all_data'])
async def show_all_info(message: Message):
    r = Redis_Preparation()
    new_users =  r.get_count_new_users()
    db = Database()
    await message.answer(text=f'За сегодня {new_users} новых пользователей')
    updated_users = r.get_count_user_updates()
    await message.answer(text=f'За сегодня {updated_users} новых запросов')
    count = db.count_users()
    await message.answer(text=f'Всего {count} пользователей')
    count = db.count_requests()
    await message.answer(text=f'Всего {count} Запросов', reply_markup=menu)
    db.close_connection()

@dp.message_handler(commands=['show_all_requests_count'])
async def count_user(message: Message):
    db = Database()
    count = db.count_requests()
    await message.answer(text=f'Всего {count} Запросов')
    db.close_connection()