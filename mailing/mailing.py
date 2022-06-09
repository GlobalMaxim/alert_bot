import redis
import json
from test import  api_parse_info
from aiogram.types import ParseMode
"""
1. При сохраненении региона пользователем, он получает уведомление о тревоге по крону (каждые 30 сек проверка).
Если тревога активна сейчас, пользователь получает уведомление, если у него is_sent_start_message = False
После получения сообщения у пользователя в "mail" меняется поле is_sent_start_message на True

"""

class Mailing():
    async def save_user_mailing(self, callback):
        user_id = callback.from_user.id
        user_region = callback.data
        user_data = {
            'user_id': user_id, 
            'user_region': user_region,
            'is_active': True,
            'is_sent_start_message': False,
            'is_sent_stop_message': False
        }
        with redis.Redis() as redis_client:
            if redis_client.get('mail') == None:
                data = {}
                data[str(user_id)] = user_data
                redis_client.set('mail', json.dumps(data))
            else:
                users_from_redis = json.loads(redis_client.get('mail'))
                users_from_redis[str(user_id)] = user_data
                redis_client.set('mail', json.dumps(users_from_redis))

    async def send_mailing(self, bot):
        regions = api_parse_info()
        with redis.Redis() as redis_client:
            users_from_redis = json.loads(redis_client.get('mail'))
            for i in regions:
                for key, values in users_from_redis.items():
                    if i['name'] == values['user_region'] and values['is_sent_start_message'] == False and i['alert'] == True:
                        # print(f'Need to send message to user {key}')
                        await bot.send_message(int(key),f'🔴<b>Повітряна тривога у "{i["name"]}"</b>\nПочаток тривоги у {i["changed"]}', parse_mode=ParseMode.HTML)
                        values['is_sent_start_message'] = True
                        values['is_sent_stop_message'] = False
                    elif i['name'] == values['user_region'] and values['is_sent_start_message'] == True and values['is_sent_stop_message'] == False and i['alert'] == False:
                        values['is_sent_stop_message'] = True
                        values['is_sent_start_message'] = False
                        await bot.send_message(int(key), f'🟢<b>Відбій повітряної тривоги у "{i["name"]}"</b>\nОновлено у {i["changed"]}', parse_mode=ParseMode.HTML)
            redis_client.set('mail', json.dumps(users_from_redis))
    
    def stop_mailing(self, callback):
        user_id = str(callback.from_user.id)
        with redis.Redis() as redis_client:
            if redis_client.get('mail') != None:
                users_from_redis = json.loads(redis_client.get('mail'))
                if user_id in users_from_redis.keys():
                    users_from_redis.pop(user_id)
                redis_client.set('mail', json.dumps(users_from_redis))
    
    def is_user_alert_active(self, user_id):
        with redis.Redis() as redis_client:
            if redis_client.get('mail') != None:
                users_from_redis = json.loads(redis_client.get('mail'))
                if str(user_id) in users_from_redis.keys():
                    return True
                else:
                    return False