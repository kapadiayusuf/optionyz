import sqlite3
from sqlite3.dbapi2 import OperationalError
import pandas as pd
import os,pathlib,json

import time
import datetime

class Database:
    parentDirectory = str(pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve())

    DB_LOCATION = parentDirectory+"/webapp/db/optionscandles.db"

    
    
    # Initializing
    def __init__(self):
        print(self.DB_LOCATION)
        self.conn = sqlite3.connect(self.DB_LOCATION,check_same_thread=False)
        self.cur = self.conn.cursor()
        try:
            

            #get the count of tables with the name
            self.cur.execute("SELECT count(*) FROM candles as total")

            # #if the count is 1, then table exists
            # if self.cur.fetchone()[0]==1 : {
            #     print('Table exists.')
            # }
            # else :
            #     print('Table does not exist.')
                        
            
        except Exception as e:
            
            if("no such table" in str(e)):
                print("NO TABLE MAMU")
                sql="CREATE TABLE candles (timestamp timestamp,symbol VARCHAR(50),open FLOAT,close FLOAT,high FLOAT,low FLOAT);"


                self.cur.execute(sql)
            else:
                print(e)


        #commit the changes to db			
        self.conn.commit()
        #close the connection
        self.conn.close()


if __name__ == '__main__':
    db = Database()
