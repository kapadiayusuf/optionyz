
import csv
from xmlrpc.client import DateTime
import pandas as pd
from datetime import date,datetime
import time
import json
import urllib, json
import urllib.parse
import requests
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup


from pytz import timezone

import os

#from macpath import split

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
]

    


class TrendLyneScraper():
    def getCOOKIE(self,url,user_agent):
        headers = {"User-Agent": user_agent,}
        result = requests.get(url, headers=headers)
        return result.cookies

    def getFilePath(self):
        # if("E:" in os.getcwd()):
        #     #return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
        #     #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
        #     return "/optionstrader/webapp/utils/"
        # else:
        #     return "/var/www/optionstrader/webapp/utils/"
        return "C://django_projects/code/optionstrader/webapp/utils/"
    
   
    
    def getDateFromTrendLyne(self):
        url="https://trendlyne.com/futures-options/futures/most-active-contract/"
        user_agent = random.choice(user_agent_list)
        cookies_jar=self.getCOOKIE("https://trendlyne.com",user_agent)
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers,cookies=cookies_jar).text
        soup = BeautifulSoup(response, "html.parser")
        # date_div=soup.find("div",{"class":"fno-trends-label"})
        # print(date_div)
        # links= date_div.find("a",{"class":"active"})
        links = soup.find("a",{"class":"active"})
               
        print("link",links)
        # return((links.text.lower().strip()))

        #return "2022-09-29"

        expiry_dates = ["2022-10-27" , "2022-11-24" , "2022-12-29" , "2023-01-26",
            "2023-02-23",  "2023-03-30","2023-04-27","2023-05-25","2023-06-29",
            "2023-07-27", "2023-08-31","2023-09-28","2023-10-26","2023-11-30",
            "2023-12-28","2024-01-25","2024-02-29","2024-03-28","2024-04-25",
            "2024-05-30","2024-06-27","2024-07-25","2024-08-29","2024-09-26",
            "2024-10-31","2024-11-28","2024-12-26" ]
            
        for d in expiry_dates:
            #dt = date.strptime(d, "%y-%m-%d") 
            #print(dt.strftime)
            
            mm = d.split('-')[1] # get month
            dd = d.split('-')[2] # get day
            yyyy= d.split('-')[0] # get year
            dt_str =  dd + '/' + mm + '/'   +  yyyy +  ' 05:23:20'
            dt_obj = datetime.strptime(dt_str, '%d/%m/%Y %H:%M:%S')
            tday = datetime.today()
            #print(str( tday))
            if (dt_obj.date() > tday.date()):
                #print (dt_obj)
                #print(tday)
                return d
            #elif(mm == current_month  and int(dd) < int(current_day))

        

    def getTrendLyneOptionScreenrs(self,scrip=''):
        datestr=self.getDateFromTrendLyne()
        
        url="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/most_active_contract/all/"
        url1="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/oi_gainers/all/"
        url2="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/oi_losers/all/"
        url3="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/long_build_up/all/"
        url4="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/short_build_up/all/"
        url5="https://trendlyne.com/futures-options/api-filter/options/"+datestr+"-near/most_active_value/all/"

        
        print(url3)

        try : 
            user_agent = random.choice(user_agent_list)
            cookies_jar=self.getCOOKIE("https://trendlyne.com",user_agent)
            headers = {"User-Agent": user_agent}

            response = requests.get(url, headers=headers,cookies=cookies_jar).text

            
            json_data=json.loads(response)

            

            response1 = requests.get(url1, headers=headers,cookies=cookies_jar).text
            json_data1=json.loads(response1)
            
            response2 = requests.get(url2, headers=headers,cookies=cookies_jar).text
            json_data2=json.loads(response2)

            response3 = requests.get(url3, headers=headers,cookies=cookies_jar).text
            json_data3=json.loads(response3)

            response4 = requests.get(url4, headers=headers,cookies=cookies_jar).text
            json_data4=json.loads(response4)

            response5 = requests.get(url5, headers=headers,cookies=cookies_jar).text
            json_data5=json.loads(response5)

        
            
            datalist=[]
            for jsn_data in [json_data,json_data1,json_data2,json_data3,json_data4,json_data5]:
                for seriesdata in jsn_data["tableData"]:
                    dt={}
                    dt["name"]=seriesdata[0]["name"]
                    dt["type"]=seriesdata[1]
                    dt["strike"]=seriesdata[2]
                    dt["price"]=seriesdata[3]
                    dt["day_change"]=seriesdata[4]
                    dt["oi"]=seriesdata[10]
                    dt["iv"]=seriesdata[12]
                    dt["vol"]=seriesdata[6]
                    dt["option_buildup"]=seriesdata[19]
                    
                    datalist.append(dt)
                    
            #print(datalist)
            df = pd.DataFrame(datalist)
            df.loc[df['name']== "NIFTY50", 'name'] = "NIFTY"
            df.loc[df['name']== "Nifty Bank", 'name'] = "BANKNIFTY"

            
            df.drop_duplicates(subset=['name', 'type','strike'],keep=False,inplace=True)

            df.sort_values(by=["name","strike"],inplace=True)
            #     if(scrip!=''):
            #         df=df[df["name"]==scrip]
            dict=  df.to_dict("records")
            # print(dict)
            return dict
        except Exception as e:
            print ("error trendlyne : ",e)
            return {}



    def  getTrendLyneHeatMap(self):
        url="https://trendlyne.com/futures-options/heatmap/all/price/"
        user_agent = random.choice(user_agent_list)
        cookies_jar=self.getCOOKIE("https://trendlyne.com",user_agent)
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers,cookies=cookies_jar).text
        soup = BeautifulSoup(response, "html.parser")
    #     <div class="draw-chart bgwhite row" id="heatmap" data-series="near" data-builtup="all" data-field="price" data-basepageurl="/futures-options/heatmap/" data-fetchurl="/futures-options/api/heatmap/27-jan-2022-near/all/price/"
        div_chart=soup.find("div",{"class","draw-chart"})
        
        # date to be hardcoded here?? 

        api_url = div_chart.get("data-fetchurl")

        json_url="https://trendlyne.com"+api_url
        result = requests.get(json_url,headers=headers,cookies=cookies_jar)
        resp_json=json.loads(result.text)
        series=resp_json["all"]["series"]
    #     "color": "#00a25bff",
    # 			"code": "NBCC",
    # 			"current_price": "50.700",
    # 			"fcp": "8.2177161",
    # 			"spot_price": "50.20",
    # 			"name": "NBCC (India) Ltd.",
    # 			"spot_change": "3.60",
    # 			"spot_difference": "7.73",
    # 			"field": "PRICE",
    # 			"field_value": "50.700",
    # 			"current_change": "8.2177161",
    # 			"current_difference": "3.85",
    # 			"oi": "22860000.000",
    # 			"oi_change": "105.2801724",
    # 			"oi_difference": "11724000.00",
    # 			"contracts": "3470.00",
    # 			"contracts_change": "6445720.43",
    # 			"contracts_difference": "3469.946166666666666666666667",
    # 			"url": "/futures-options/derivative/27-jan-2022-near/916/NBCC/nbcc-india-ltd/",
    # 			"basis": "0.500",
    # 			"builtup_str": "Long Build Up"
        fields=["code","name","color","current_price","current_change","current_difference","oi","oi_change","oi_difference", \
                "contracts","contracts_change","contracts_difference","builtup_str"]
        datalist=[]
        for seriesdata in series:
            dt={}
            for f in fields:
                dt[f]=seriesdata[f]
            datalist.append(dt)
            
    #     print(datalist)
        df = pd.DataFrame(datalist)
        #df.loc[df['code']== "NIFTY50", 'code'] = "NIFTY"
        #df.loc[df['code']== "NIFTYBANK", 'code'] = "BANKNIFTY"
        
        df["oi_change"] = pd.to_numeric(df["oi_change"])
        df["oi"] = pd.to_numeric(df["oi"])
        df["current_price"] = pd.to_numeric(df["current_price"])
        df["current_change"] = pd.to_numeric(df["current_change"])
        df["current_difference"] = pd.to_numeric(df["current_difference"])
        df["oi_difference"] = pd.to_numeric(df["oi_difference"])
        df["contracts"] = pd.to_numeric(df["contracts"])
        df["contracts_change"] = pd.to_numeric(df["current_change"])
        df["contracts_difference"] = pd.to_numeric(df["contracts_difference"])
        
        
        # df_lots=pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+"/optionstrader/webapp/utils/options_lots.csv")

        
        #df_lots=pd.read_csv("options_lots.csv")
        #production
        df_lots=pd.read_csv(self.getFilePath()+"options_lots.csv")


        # result_df = pd.merge(df, df_lots, on="code")  
        result_df = df.merge(df_lots, left_on='code', right_on='code', how='left')
        result_df["atm"]=result_df["current_price"]-result_df["current_price"]%result_df["contract_step"]
        result_df["citm1"]=result_df["atm"]-1*result_df["contract_step"]
        result_df["citm2"]=result_df["atm"]-2*result_df["contract_step"]
        result_df["citm3"]=result_df["atm"]-3*result_df["contract_step"]
        result_df["citm4"]=result_df["atm"]-4*result_df["contract_step"]
        result_df["pitm1"]=result_df["atm"]+1*result_df["contract_step"]
        result_df["pitm2"]=result_df["atm"]+2*result_df["contract_step"]
        result_df["pitm3"]=result_df["atm"]+3*result_df["contract_step"]
        result_df["pitm4"]=result_df["atm"]+4*result_df["contract_step"]
        dict=  result_df.to_dict("records")
        #print(dict)
        return dict


tsc = TrendLyneScraper()
gtdate = tsc.getDateFromTrendLyne()
dt = tsc.getTrendLyneHeatMap()

