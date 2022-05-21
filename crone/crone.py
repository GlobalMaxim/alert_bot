import aioschedule
import asyncio
import datetime
from config import admin_id
from db.database import Database
# from telebot import dp, bot

def printer():
    print('1')

def execute_script():
    db = Database
    db.save_data_to_db()

async def send_message_to_admin(bot):
    await bot.send_message(admin_id, 'Crone completed')

async def scheduler(bot):
    aioschedule.every().day.at('02:00').do(execute_script)
    aioschedule.every().day.at('02:00').do(send_message_to_admin, bot=bot)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

