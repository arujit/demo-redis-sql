import socket
import pickle
import sys,os
import time

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        

    def connect(self):
        host = "127.0.0.1"
        port = 10007
        self.sock.connect((host,port))

    def send(self,data):
        self.sock.send(data)

           
    def close(self):
        self.sock.close()

        
if __name__ == "__main__":
    dict = {"Task": "ADD","user_name":"user-5","user_password":"password-5"}
    cli = Client()
    cli.connect()
    cli.send(pickle.dumps(dict))
    print "Blah! Blah"
    #time.sleep(100)
    ack = cli.sock.recv(512)
    print ack