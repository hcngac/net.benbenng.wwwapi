import sqlite3
import os.path
import shutil
import mysql.connector

class Database:
    def __init__(self, initialize:bool=False):
        try:
            self.connection = mysql.connector.connect(host="db.www.benbenng.net",
                user="siteMaster", 
                passwd="tz6e2nbegg")
            cursor = self.connection.cursor()
            if initialize:
                with open("initDb.sql") as f:
                    for line in f:
                        cursor.execute(line)
            cursor.close()
            self.database = "net_benbenng_www"
        except e:
            raise e
        
    def __del__(self):
        self.connection.close()
    def execute(self, query: str, parameters: tuple):
        cursor = self.connection.cursor()
        cursor.execute("USE " + self.database)
        cursor.execute(query, parameters)
        try:
            results = cursor.fetchall()
        except e:
            results = None
        cursor.close()
        return results
    def commit(self):
        self.connection.commit()
    def rollback():
        self.connection.rollback();



