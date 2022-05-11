from aiogram import Bot, Dispatcher, executor
import asyncio
from config import TOKEN

# loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')

dp = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)