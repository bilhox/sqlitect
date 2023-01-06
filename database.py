import sqlite3
import os

class Database:

    def __init__(self , database_path : str , overwrite=False):

        if(overwrite and os.path.exists(database_path)):
            os.remove(database_path)

        self._connector = sqlite3.connect(database_path)
        self._cursor = self._connector.cursor()
    
    def createTable(self , table : str , attributes : dict , primary_keys=[]):

        sqlQuery = "CREATE TABLE "+table+" ( "
        n = 1
        for key , valueType in attributes.items():
            sqlQuery += key + " "
            sqlQuery += valueType
            
            sqlQuery += " , " if(n != len(attributes)) else ""

            n+=1
        
        if(primary_keys):
            n = 1
            sqlQuery += " , PRIMARY KEY ( "
            for key in primary_keys:
                sqlQuery += key+" "
                if(n != len(primary_keys)):
                    ", "
                n+=1
            sqlQuery += ") "
        sqlQuery += " )"

        self._cursor.execute(sqlQuery)
    
    def loadTable(self , csv_path : str , table_name : str):
        
        # Hidden import , hehe
        from csv import DictReader

        entries = []

        with open(file=csv_path , newline='' , encoding='utf8') as reader:
            spam_reader = DictReader(reader , delimiter=';')
            for entry in spam_reader:
                entries.append(entry)
        
        attributes = {att:"TEXT" for att in entries[0].keys()}
        self.createTable(table_name , attributes)

        datas = [list((entry.values())) for entry in entries]
        self._cursor.executemany("INSERT INTO "+table_name+" VALUES ( ? "+", ?"*(len(attributes)-1)+" )" , datas)
        self._connector.commit()
    
    def getTableAttributes(self , table : str):
        res = self._cursor.execute("SELECT * FROM "+table)
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
            if(isinstance(value , str)):
                sqlQuery += "'"
            sqlQuery += str(value)
            if(isinstance(value , str)):
                sqlQuery += "'"
            if(len(keys)==i):
                sqlQuery += " ) "
            else:
                sqlQuery += " , "
            i+=1
        
        self._cursor.execute(sqlQuery)
        self._connector.commit()
    
    def fetch(self , table ,  attributes=[] , distinct=False , condition=None):
        sqlQuery = "SELECT "
        if(distinct):
            sqlQuery += "DISTINCT "
        
        if(attributes):
            i = 1
            for attribute in attributes:
                sqlQuery += attribute + " "
                if(i != len(attributes)):
                    sqlQuery += ", "
                i+=1
        else:
            sqlQuery += " *"

        sqlQuery += "FROM "+table

        if(condition):
            sqlQuery += " WHERE "+condition

        res = self._cursor.execute(sqlQuery)
        return res.fetchall()
    
    def deleteTable(self , table : str):
        self._cursor.execute("DROP TABLE "+table)
    
    def deleteFromTable(self , table : str , condition=None):
        sqlQuery = "DELETE FROM "+table
        if(condition):
            sqlQuery += " WHERE "+condition
        self._cursor.execute(sqlQuery)
    
    def updateFromTable(self , table : str , modifications : list[str], condition=None):
        sqlQuery = "UPDATE "+table+" SET "+modifications[0]

        for i in range(1,len(modifications)):
            sqlQuery += " , "+modifications[i]

        if(condition):
            sqlQuery += " WHERE "+condition
        self._cursor.execute(sqlQuery)
        self._connector.commit()
    
    def addAttribute(self , table : str , attribute_name : str , attribute_type : str):
        sqlQuery = "ALTER TABLE "+table+" ADD "+attribute_name+" "+attribute_type
        self._cursor.execute(sqlQuery)
    
    def deleteAttribute(self , table : str , attribute_name : str):
        self._cursor.execute(f"ALTER TABLE {table} DROP {attribute_name}")
    
    def executeSQLFile(self , path : str):
        script = ""

        with open(path , mode="r" , encoding="utf8" , newline="") as reader:
            for line in reader.readlines():
                script += line

        self._cursor.executescript(script)
        self._connector.commit()
