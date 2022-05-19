from datetime import datetime
import redis
import json
import logging

class Redis_Preparation():

    logging.basicConfig(level=logging.WARNING, filename='log/redis-log.txt')
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

        except Exception :
            logging.exception('\n'+'Get regions from redis error! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
    def create_new_user_to_redis(self,message):
        try:
            redis_client = redis.Redis(db=1)
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            language_code = message.from_user.language_code
            user_data = {
                'user_id':user_id, 
                'first_name': first_name, 
                'last_name': last_name, 
                'username': username, 
                'language_code': language_code, 
                'count_exec_script': 0,
                'created_at':str(datetime.now().strftime("%d-%m-%Y %H:%M")), 
                'modified_at': str(datetime.now().strftime("%d-%m-%Y %H:%M"))
            }

            if redis_client.get('users') is None:
                data = {}
                data[user_id] = user_data
                redis_client.set('users', json.dumps(data))
            else:
                users_from_redis = json.loads(redis_client.get('users'))
                if str(user_id) not in users_from_redis.keys():
                    users_from_redis[user_id] = user_data
                    redis_client.set('users', json.dumps(users_from_redis))

        except:
            logging.exception('\n'+'Create new user error! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
    def create_user_updates_to_redis(self, message):
        try:
            redis_client = redis.Redis(db=1)
            user_id = message.from_user.id
            user_data = {
                'user_id':user_id,
                'count_exec_script': 1, 
                'modified_at': str(datetime.now().strftime("%d-%m-%Y %H:%M"))
            }
            if redis_client.get('updates') is None:
                data = {}
                data[user_id] = user_data
                redis_client.set('updates', json.dumps(data))
            else:
                updates_from_redis = json.loads(redis_client.get('updates'))
                
                if str(user_id) in updates_from_redis.keys():
                    updates_from_redis[str(user_id)]['count_exec_script'] += 1
                    updates_from_redis[str(user_id)]['modified_at'] = str(datetime.now().strftime("%d-%m-%Y %H:%M"))
                    redis_client.set('updates', json.dumps(updates_from_redis))
                else:
                    updates_from_redis[user_id] = user_data
                    redis_client.set('updates', json.dumps(updates_from_redis))
        except:
            logging.exception('\n'+'Create user updates error! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        
    def get_new_users_from_redis(self):
        redis_client = redis.Redis(db=1)
        if (redis_client.get('users')) != None:
            users = json.loads(redis_client.get('users'))
            # print(users)
            return users
    
    def get_new_updates_from_redis(self):
        redis_client = redis.Redis(db=1)
        if (redis_client.get('updates')) != None:
            users = json.loads(redis_client.get('updates'))
            return users


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
    

# r = Redis_Preparation()
# print(r.get_new_users_from_redis())