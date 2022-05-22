import aioschedule
import asyncio
from config import admin_id
from db.database import Database

values = []

async def execute_script():
    global values
    db = Database()
    values = db.save_data_to_db()

async def send_message_to_admin(bot):
    await bot.send_message(admin_id, f'Сохранено {values[0]} новых пользователей и обновлено {values[1]} старых пользователя')

async def scheduler(bot):
    aioschedule.every().day.at('01:59').do(execute_script)
    aioschedule.every().day.at('02:00').do(send_message_to_admin, bot=bot)
    
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

