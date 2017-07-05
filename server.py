import socket
import MySQLdb
import mysql.connector
import os,sys
import pickle
from redisApi import RedisApi

"""
This is the basic server side python script for python coneection with Mysql db.
Basic idea - Let's take a socket server for considiration
---- It is on a loop seeking client connection
---- after client connected it tells to connect with the data server
---- It uses some api to fetch info from data server and intermediate cache server
---- Mainthrad listens for client calls and proper threads are created accoring to client requests
"""

sql_config = {
    'user': 'root',
    'password': 'Arujit@17',
    'host': '127.0.0.1',
    'database': 'login',
    'raise_on_warnings': True,
}


#connection = mysql.connector(**config)

class Communication:
    """ TCP Server initialization"""
    def __init__(self):
        host  = "127.0.0.1"
        port = 10007
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.server.listen(1)
        print "server set-up finished"

    def close(self):
        self.server.close()

    def send(self,data):
        print "gonna send data"
        self.server.send(data)    


class Db:
    """Class to handel all dbs"""
    def __init__ (self,message):
        self.sqlConfig = sql_config
        self.message = message
        print self.message
        self.api = RedisApi(6379,0)
        
    def _sql_connect(self):
        self.connection = mysql.connector.connect(**self.sqlConfig)    
        return self.connection
        
    def add_sql(self,connection,cursor,message):
        self.add_user  = (" INSERT INTO Userinfo "
                     "(userId,userName,userPassword)"
                     "VALUES (NULL,%(user_name)s,%(user_password)s )"
                      )
        self.connection = connection
        self.cursor = cursor
        self.message = message
        self.cursor.execute(self.add_user,self.message)
        self.connection.commit()
        
    def add_redis(self,message):
        self.token = message    
        del self.token["Task"]
        self.user_name = self.message["user_name"]
        self.api.create_user(self.user_name,self.token)
        
    def process(self):
        self.connection = self._sql_connect()
        print "connection established with sql !!!"
        self.cursor = self.connection.cursor()
        if self.message['Task'] == 'ADD':
            self.add_sql(self.connection,self.cursor,self.message)
            print "Added to sql Db"
            self.resp = "Added!!!"
            self.redis_resp = self.add_redis(self.message)
        return self.resp

if __name__ == "__main__":
    """Main thread"""
    check_server = Communication()
    while True:
        #print "true"
        client,address = check_server.server.accept()
        """message is a dictionary that has some attributes like what to do, username and password """ 
        client_pickle = client.recv(512)
        message = pickle.loads(client_pickle)
        db = Db(message)
        resp = db.process()
        client.send(resp)
