import redis

class Cache:
    def __init__(self):
        self.redis = redis.StrictRedis(host='cache.www.benbenng.net', port=6379)