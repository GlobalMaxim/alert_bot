from aiogram import Bot, Dispatcher, executor
from config import TOKEN

bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

def on_shutdown():
    dp.storage.close()

if __name__ == '__main__':
    from handlers.admin_handlers import send_to_admin
    from handlers.handlers import dp
    executor.start_polling(dp, on_startup=send_to_admin)