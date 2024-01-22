
import csv
from xmlrpc.client import DateTime
import openpyxl
import pandas as pd
from datetime import date,datetime , timedelta
import time
import json
import requests
import random
import os
import difflib

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions




class niftytraderdata:
    def __init__(self):
        pass
    
    def getFilePath(self):
        # if("E:" in os.getcwd()):
        #     #return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
        #     #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
        #     return "/optionstrader/webapp/utils/"
        # else:
        #     return "/var/www/optionstrader/webapp/utils/"
        return "C://django_projects/code/optionstrader/webapp/utils/"    
   
   
    def updatebanlist(self):
        link = "https://webapi.niftytrader.in/webapi/Resource/ban-list"
        
        jsondata = requests.get(link).json()
        #print (jsondata)
        
        if (jsondata['resultMessage'] == "Success"):
            jsondata = jsondata['resultData']
            
            #print to file 
            df_banlist = pd.DataFrame(jsondata['securities_ban_result'])
            df_possible_entrants = pd.DataFrame(jsondata['possible_entrants_result'])
            df_possible_exits = pd.DataFrame(jsondata['possible_exits_result'])
            json_date = jsondata['date']
            
            df_all = pd.DataFrame(jsondata['all_list_result'])
            
            #add a date column
            df_banlist.insert(0, 'Date', json_date)
            df_possible_entrants.insert(0, 'Date', json_date)
            df_possible_exits.insert(0, 'Date', json_date)
            
            df_banlist["BAN_STATUS"] = "BANNED"
            df_possible_entrants["BAN_STATUS"] = "POTENTIAL_ENTRANT"
            df_possible_exits["BAN_STATUS"] = "POTENTIAL_EXIT"
            
            df = pd.concat([df_banlist, df_possible_entrants , df_possible_exits], ignore_index=True)
            merged_df = pd.merge(df_all , df[['symbol_name', 'BAN_STATUS']], on=['symbol_name'], how='left')
            #print ( df_banlist , "\n\n" , df_possible_entrants , "\n\n" , df_possible_exits) 
            
            # df_banlist.to_excel(self.getFilePath()+"Output/ban-list.xlsx")
            # df_possible_entrants.to_excel(self.getFilePath()+"Output/ban-list_possible_entrants.xlsx")
            # df_possible_exits.to_excel(self.getFilePath()+"Output/ban-list_possible_exits.xlsx")
            
            merged_df.to_excel(self.getFilePath()+"Output/ban-list.xlsx")
        
        else : 
            print ( "Error in getting ban list" )
            
            
                
        
if __name__ == '__main__':
    obj = niftytraderdata()
    obj.updatebanlist()