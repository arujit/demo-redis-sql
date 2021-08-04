import socket
import pickle
import requests
import sys,os
import time
import yaml

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        

    def connect(self):
        host = "127.0.0.1"
        port = 10014

        with open("sql_config.yaml","r") as configfile:
            self.config_file = yaml.load(configfile)
        self.tcp_config = self.config_file["tcp"]
        self.sock.connect((self.tcp_config["host"],self.tcp_config["port"]))

    def send(self,data):
        self.sock.send(data)

           
    def close(self):
        self.sock.close()

        
if __name__ == "__main__":
    message = {"Task": "ADD","UserInfo":{"user_name":"user-9","user_password":"password-9"}}
    cli = Client()
    cli.connect()
    cli.send(pickle.dumps(message))
    print "Blah! Blah"
    #time.sleep(100)
    ack = cli.sock.recv(512)
    print ack
