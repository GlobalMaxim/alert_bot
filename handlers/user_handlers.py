from aiogram.types import ParseMode
from telebot import dp, bot
from aiogram.types import Message
from config import admin_id
from aiogram.types import Message, BotCommand, BotCommandScopeChatAdministrators
from aiogram.dispatcher.filters import Command, Text
from keyboards.default.menu import menu
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from redisPreparation import Redis_Preparation
from db.database import add_new_user
from test_windows import  parse_photo, api_parse_info
from utils.misc.throttling import rate_limit

# async def send_to_admin(dp):
#     await bot.send_message(admin_id, 'Бот запущен', reply_markup=menu)
#     await bot.set_my_commands([
#         BotCommand(command='/restart', description='Перезапустить')
#     ])
#     await bot.set_my_commands([
#         BotCommand('show_users_count', 'Колличество пользователей'),
#         BotCommand('show_all_requests_count', 'Всего запросов')
#     ])

@dp.message_handler(Text(equals=["/restart"]))
@dp.message_handler(CommandStart())
async def register_user(message: Message):
    chat_id = message.from_user.id
    name = message.from_user.first_name
    await bot.send_message(chat_id=chat_id, text=f'Привіт, {name}', reply_markup=menu)

@dp.message_handler(Text(equals=["Отримати карту повітряних тривог"]))
@rate_limit(limit=10)
async def run(message: Message):
    
    if str(message.from_user.id) != admin_id:
        notify_admin=f"Пользователь с ником @{message.from_user.username}, {message.from_user.first_name} воспользовался ботом"
        await bot.send_message(admin_id, text=notify_admin, disable_notification=True)
    await message.answer('Зачекайте...')
    exec_redis = Redis_Preparation()
    api_data = api_parse_info()
    res = exec_redis.get_regions_from_redis(api_data)
    await message.answer('Тривоги працюють в наступних областях:')
    for key,value in res['regions'].items():
        await message.answer(f"<b>{key}</b>\nПочаток тривоги у {value}", parse_mode=ParseMode.HTML)
    await message.answer('Зачекайте, завантажується фото...')
    if res['is_updated'] == True:
        parse_photo()
    await message.answer_photo(photo=open('screenshot.png', 'rb'), reply_markup=menu)
    # exec_redis.set_temp_data_to_redis(message)
    add_new_user(message)

@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/restart - Перезапустить'
    ]
    await message.answer('\n'.join(text))

@dp.message_handler(Text('Слава Україні!🇺🇦'))
async def register_user(message: Message):
    await message.answer('Героям Слава!🇺🇦')

@dp.message_handler()
async def register_user(message: Message):
    chat_id = message.from_user.id
    name = message.from_user.username
    await bot.send_message(chat_id=chat_id, text=f'{name}, спробуйте ще раз', reply_markup=menu)

