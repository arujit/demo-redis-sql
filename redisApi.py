import redis
import yaml

"""
Single threaded redis api for handeleing the db

hashmap for a user
"""

class RedisApi(object):
    def __init__(self):
        print "hello RedisApi"
        with open("sql_config.yaml","r") as configfile:
            self.config_file = yaml.load(configfile)
            
        self.redis_config = self.config_file["redis"]
        self.pool = redis.ConnectionPool(host=self.redis_config["host"],port=self.redis_config["port"],db = self.redis_config["db"])
        self.r = redis.Redis(connection_pool = self.pool)
        print "Welcome to Redis"
        
    def create_user(self,name,tokens):
        self.key = name
        self.token = tokens
        print self.key
        #self.username = name
        self.r.hset(self.key,'created',True)
        self.r.hmset(self.key,self.token)
        #self.r.lpush('user',self.key)
        self.r.sadd('user',self.key)
        return True

    

