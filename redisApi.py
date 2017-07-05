import redis


"""
Single threaded redis api for handeleing the db

hashmap for a user
"""

class RedisApi(object):
    def __init__(self,port,db_no):
        self.host = 'localhost'
        self.port = port
        #print "hello RedisApi"
        self.db = db_no
        self.pool = redis.ConnectionPool(host = self.host,port = self.port,db = self.db )
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

    

