import imp
from telebot import dp, bot
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from config import admin_id
from keyboards.default.menu import menu
from aiogram.dispatcher.filters import Command, Text
from db.database import count_users, count_requests, save_data
from telegram_redis.redisPreparation import Redis_Preparation 

async def send_to_admin(dp):
    import middlewares
    middlewares.setup(dp)
    await bot.send_message(admin_id, 'Бот запущен', reply_markup=menu)
    await bot.set_my_commands([
        BotCommand(command='/restart', description='Перезапустить')
    ], scope=BotCommandScopeDefault())
    await bot.set_my_commands([
        BotCommand('show_users_count', 'Колличество пользователей'),
        BotCommand('show_all_requests_count', 'Всего запросов'),
        BotCommand('save', 'Сохранить данные'),
        # BotCommand('append', 'ОБновить пользователей')
    ], scope=BotCommandScopeChat(chat_id=admin_id))

@dp.message_handler(commands=['show_users_count'])
async def count_user(message: Message):
    count = count_users()
    await message.answer(text=f'Всего {count} пользователей', reply_markup=menu)

@dp.message_handler(commands=['save'])
async def reset(message: Message):
    save_data()
    # r = Redis_Preparation()
    # r.create_new_user_to_redis(message)
    # r.get_new_users_from_redis()

# @dp.message_handler(commands=['append'])
# async def reset(message: Message):
    # r = Redis_Preparation()
    # r.create_user_updates_to_redis(message)
    # r.get_new_updates_from_redis()
    # await message.answer(text=f'Всего {count} пользователей', reply_markup=menu)

@dp.message_handler(commands=['show_all_requests_count'])
async def count_user(message: Message):
    count = count_requests()
    await message.answer(text=f'Всего {count} Запросов', reply_markup=menu)