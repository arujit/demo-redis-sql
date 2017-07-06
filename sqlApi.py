import MySQLdb
import mysql.connector
import yaml

"""
dummy sql API for user addition in SQL DB

"""

class MysqlApi:
    def __init__(self):
        with open("sql_config.yaml","r") as configfile:
            self.config_file = yaml.load(configfile)

        self.sql_config = self.config_file["mysql"]

        """
        connection to the sql  db when ever db is called
        """
        self.connection = mysql.connector.connect(**self.sql_config)

        self.cursor = self.connection.cursor()
        
    def add_sql(self,message):
        add_message = message
        add_user  = (" INSERT INTO Userinfo "
                     "(userId,userName,userPassword)"
                     "VALUES (NULL,%(user_name)s,%(user_password)s )"
                      )
        self.cursor.execute(add_user,add_message["UserInfo"])
        self.connection.commit()
        return True
