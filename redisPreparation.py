from datetime import datetime
import redis
import json

class Redis_Preparation():
    # def __init__(self, result):
    #     self.result = result
    
    def get_regions_from_redis(self, data):
        try:
            redis_client = redis.Redis()
            reg_from_redis = redis_client.get('reg')
            regs = data
            result = {}
            if reg_from_redis is None or json.loads(reg_from_redis) != regs:
                redis_client.set('reg', json.dumps(regs))
                result['regions'] = regs
                result['is_updated'] = True
                print('Updated')
            else:
                not_updated = json.loads(reg_from_redis)
                result['regions'] = not_updated
                result['is_updated'] = False
            return result
        except Exception as ex:
            with open('log/redis-log.txt', 'a') as file:
                file.write(str(ex))
    
    def set_temp_data_to_redis(self, message):
        try:
            redis_client = redis.Redis(db=1)
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            language_code = message.from_user.language_code

            user_from_redis = redis_client.get(str(user_id))

            
            if user_from_redis is None:
                user_data = {'user_id':user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'language_code': language_code, 'count_exec_scripts': 1, 'modified_at': str(datetime.now())}
                redis_client.set(str(user_id), json.dumps(user_data))
            else:
                user_data_from_redis = json.loads(user_from_redis)
                user_data_from_redis['count_exec_scripts'] += 1
                user_data_from_redis['modified_at'] = str(datetime.now())
                redis_client.set(str(user_id), json.dumps(user_data_from_redis))
        except Exception as ex:
            with open('log/redis-log.txt', 'a') as file:
                file.write(str(ex))
    
    def get_users_data_from_redis():
        try:
            redis_client = redis.Redis(db=1)
        except Exception as ex:
            with open('log/redis-log.txt', 'a') as file:
                file.write(str(ex))
