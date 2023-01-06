import sqlite3
import os


class DatabaseCommunicator:

    def __init__(self , database_path : str , overwrite=False):

        if(overwrite and os.path.exists(database_path)):
            os.remove(database_path)

        self.connector = sqlite3.connect(database_path)
        self.cursor = self.connector.cursor()
    
    def createTable(self , table : str , attributes : dict , typeInterpreted=True):

        sqlQuery = "CREATE TABLE "+table+" ( "
        n = 1
        for key , valueType in attributes.items():
            sqlQuery += key + " "
            if(typeInterpreted):
                if(valueType is int):
                    sqlQuery += "BIGINT"
                elif(valueType is str):
                    sqlQuery += "LONGTEXT"
                else:
                    raise TypeError("Value type not supported by SQL \n\tSuggestions:\n\t\tSet typeInterpreted parameter to false and use specific types !")
            else:
                sqlQuery += key + " "
                sqlQuery += valueType
            
            sqlQuery += " , " if(n != len(attributes)) else " )"

            n+=1

        self.cursor.execute(sqlQuery)
    
    def fetchAll(self , table : str):
        res = self.cursor.execute("SELECT * FROM "+table)
        return res.fetchall()
    
    def getTableAttributes(self , table : str):
        res = self.cursor.execute("SELECT * FROM "+table)
        return [att[0] for att in res.description]
    
    def insert(self , table : str , entry : dict):
        sqlQuery = "INSERT INTO "+table+"( "
        keys = entry.keys()
        values = entry.values()

        i = 1
        for key in keys:
            sqlQuery += key
            if(len(keys)==i):
                sqlQuery += " ) "
            else:
                sqlQuery += " , "
            i+=1

        sqlQuery += "VALUES ( "

        i = 1
        for value in values:
            sqlQuery += str(value)
            if(len(keys)==i):
                sqlQuery += " ) "
            else:
                sqlQuery += " , "
            i+=1
        
        print(sqlQuery)
        self.cursor.execute(sqlQuery)
        self.connector.commit()

    
    def fetch(self , table ,  attributes=[]):
        sqlQuery = "SELECT "
        for attribute in attributes:
            sqlQuery += attribute + " "
        sqlQuery += "FROM "+table
        res = self.cursor.execute(sqlQuery)
        return res.fetchall()
    
db = DatabaseCommunicator("database.db" , overwrite=True)
db.createTable("users"  , {"user_id":"INT UNSIGNED" , "username":"CHAR(40)" , "password":"CHAR(40)"} , typeInterpreted=False)
db.fetch("users" , ["user_id" , "username"])
db.insert("users" , {"user_id":1 , "username":"lody" , "password":"admin"})