from datetime import datetime
from aiogram.types import ParseMode
from mailing.mailing import Mailing
from telebot import dp, bot
from aiogram.types import Message
from config import admin_id
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from keyboards.default.menu import menu, menu_2
from keyboards.mailing.regionsMarkup import regions_markup
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from telegram_redis.redisPreparation import Redis_Preparation

from utils.misc.throttling import rate_limit


@dp.message_handler(CommandStart())
async def register_user(message: Message):
    r = Redis_Preparation()
    r.create_new_user_to_redis(message)
    chat_id = message.from_user.id
    name = message.from_user.first_name
    mail = Mailing()
    is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
    if is_user_uses_alert == True:
        markup = menu_2
    else:
        markup = menu
    await bot.send_message(chat_id=chat_id, text=f'Привіт, {name}', reply_markup=markup)

@dp.message_handler(Text(equals=["/restart"]))
async def register_user(message: Message):
    mail = Mailing()
    is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
    if is_user_uses_alert == True:
        markup = menu_2
    else:
        markup = menu
    chat_id = message.from_user.id
    name = message.from_user.first_name
    await bot.send_message(chat_id=chat_id, text=f'Привіт, {name}', reply_markup=markup)

@dp.message_handler(Text(equals=["🗺Отримати карту повітряних тривог"]))
@rate_limit(limit=10)
async def run(message: Message):
    mail = Mailing()
    is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
    if is_user_uses_alert == True:
        markup = menu_2
    else:
        markup = menu
    if message.from_user.id != admin_id:
        notify_admin=f"Пользователь с ником @{message.from_user.username}, {message.from_user.first_name} воспользовался ботом"
        await bot.send_message(admin_id, text=notify_admin, disable_notification=True)
    
    r = Redis_Preparation()
    res = r.get_regions_from_redis()
    current_date = str(datetime.now().strftime('%H:%M %d-%m-%Y'))
    if len(res['regions']) > 0:
        await message.answer('Тривоги працюють в наступних областях:')
        for i in res['regions']:
            await message.answer(f"🛑 <b>{i['name']}</b>\nПочаток тривоги у {i['changed']}\n@ukraine_alarm_bot", parse_mode=ParseMode.HTML)
        
        await message.answer_photo(photo=open('screenshot.png', 'rb'), caption=f"<b>❗️Карта повітряних тривог станом на {current_date}</b>\n@ukraine_alarm_bot", reply_markup=markup)
    else:
        await message.answer('Тривог зараз немає!')
    r.create_user_updates_to_redis(message)

@dp.message_handler(commands=['set'])
@dp.message_handler(Text(equals=["📢Увімкнути повідомлення про тривогу"]))
async def send_mail(message: Message):
    await message.answer(text='📍Оберіть місце, де ви знаходитесь:', reply_markup=regions_markup)

@dp.callback_query_handler()
async def save_user_region(call: CallbackQuery):
    mail = Mailing()
    if call.data == 'cancel':
        await call.message.edit_reply_markup()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text= f'❗️Ви не обрали регіон')
        
        mail.stop_mailing(call)
    else:
        await call.message.edit_reply_markup()
        await mail.save_user_mailing(call)
        await bot.send_message(chat_id=call.from_user.id, text= f'✅Вітаю, ви будете отримумати сповіщення при повітряній тривозі у <b>"{call.data}"</b>', parse_mode=ParseMode.HTML, reply_markup=menu_2)
        await mail.check_is_active_user_region(bot,call)
    await call.answer()

@dp.message_handler(Text(equals=["❌Вимкнути сповіщення про тривогу"]))
async def send_mail(message: Message):
    mail = Mailing()
    await message.answer(text='❗️Ви не будете отримувати сповіщення про тривоги', reply_markup=menu)
    mail.stop_mailing(message)
    

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
    mail = Mailing()
    is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
    if is_user_uses_alert == True:
        markup = menu_2
    else:
        markup = menu
    chat_id = message.from_user.id
    name = message.from_user.first_name
    await bot.send_message(chat_id=chat_id, text=f'{name}, спробуйте ще раз', reply_markup=markup)


