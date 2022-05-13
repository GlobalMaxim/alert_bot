import redis
import json

class Redis_Preparation():
    # def __init__(self, result):
    #     self.result = result
    
    def get_data_from_redis(self, data):
        redis_client = redis.Redis()
        reg_from_redis = redis_client.get('reg')
        regs = data
        result = {}
        if reg_from_redis is None or json.loads(reg_from_redis) != regs:
            # redis_client.delete('reg')
            redis_client.set('reg', json.dumps(regs))
            # updated = json.loads(reg_from_redis)
            result['regions'] = regs
            result['is_updated'] = True
            print('Updated')
        else:
            not_updated = json.loads(reg_from_redis)
            result['regions'] = not_updated
            result['is_updated'] = False
        return result
