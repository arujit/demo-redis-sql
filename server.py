import socket
import MySQLdb
import mysql.connector
import os,sys
import pickle
from redisApi import RedisApi
import yaml
from sqlApi import MysqlApi

"""
This is the basic server side python script for python coneection with Mysql db.
Basic idea - Let's take a socket server for considiration
---- It is on a loop seeking client connection
---- after client connected it tells to connect with the data server
---- It uses some api to fetch info from data server and intermediate cache server
---- Mainthrad listens for client calls and proper threads are created accoring to client requests
TO_D0 :
-*- finish config
-*- sql handel api
--- multi threading
--- Make code robust
///
--- finish call backs and transactions
--- architecture handeling

"""

class Communication:
    """ TCP Server initialization"""
    def __init__(self):
        with open("sql_config.yaml","r") as configfile:
            self.config_file = yaml.load(configfile)

        self.tcp_config = self.config_file["tcp"]
        print self.tcp_config     
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.tcp_config["host"],self.tcp_config["port"]))
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
        self.message = message
        print self.message
        self.redis_api = RedisApi()
        self.sql_api = MysqlApi()

    def add_sql(self,message):
        return self.sql_api.add_sql(message)
       
    
    def add_redis(self,message):
        self.token = message    
        del self.token["Task"]
        self.user_name = self.message["user_name"]
        self.redis_api.create_user(self.user_name,self.token)
        
    def process(self):
        #self.connection = self._sql_connect()
        #print "connection established with sql !!!"
        #self.cursor = self.connection.cursor()
        if self.message['Task'] == 'ADD':
            self.sql_resp = self.add_sql(self.message)
            if self.sql_resp == True:
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
