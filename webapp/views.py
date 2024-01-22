import datetime
import os
from django.http.response import HttpResponse, JsonResponse 
from django.http import HttpResponseRedirect 
from django.shortcuts import render , redirect

from django.urls import reverse

from django.views.decorators.http import require_GET
from webapp.utils.opstrascraper import OpstraScraper

from webapp.utils.apimanager import ApiManager

from webapp.utils.optionscron import OptionsCron
from webapp.utils.niftytraderdata import niftytraderdata
import pandas as pd
import requests


from django.views.decorators.csrf import csrf_exempt
import json



def getFilePath():
        # if("E:" in os.getcwd()):
        #     #return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
        #     #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
        #     return "/optionstrader/webapp/utils/"
        # else:
        #     return "/var/www/optionstrader/webapp/utils/"
    return "C://django_projects/code/optionstrader/webapp/utils/"


@csrf_exempt
def webhook_VSLRT(request):
    print ("webhooked!")
    if request.method == 'POST':
        # Assuming the payload is sent as JSON
        print ("method post!")
        try:
            print("try block")
            req = str(request.body)
            json_payload = req.split("{",maxsplit= 1 )[1]
            json_payload = json_payload.split("}",maxsplit= 1 )[0]
            #print(json_payload)
                    
            split_json_list = json_payload.split(";")
                       
            df = pd.DataFrame()
            
            ############## List 1 : RegrVWAPCrossUP_list: None,NSE:BHARTIARTL1!,NSE:COALINDIA1!
            RegrVWAPCrossUP_str = split_json_list[0].split(":", maxsplit=1)[1]
            
            RegrVWAPCrossUP_list = RegrVWAPCrossUP_str.split(",")
            
            #print(RegrVWAPCrossUP_list)         
            
             ############## List 2 : RegrVWAPCrossDN_list: None,NSE:BHARTIARTL1!,NSE:COALINDIA1!
            RegrVWAPCrossDN_str = split_json_list[1].split(":", maxsplit=1)[1]
            
            RegrVWAPCrossDN_list = RegrVWAPCrossDN_str.split(",")
            
            #print(RegrVWAPCrossDN_list)
            
            ############## List 3 : greenCloud_list:None,NSE:DIVISLAB1!,NSE:CIPLA1!,NSE:ALKEM1!,NSE:LUPIN1!,NSE:BIOCON1!,NSE:ABBOTINDIA1!,NSE:LALPATHLAB1!,NSE:SYNGENE1! 
            greenCloud_str = split_json_list[2].split(":", maxsplit=1)[1]
            greenCloud_list = greenCloud_str.split(",")
            print(greenCloud_list)
            
            
            ############## List 4 : redCloud_list:None,NSE:SUNPHARMA1!,NSE:DRREDDY1!,NSE:APOLLOHOSP1!,NSE:PEL1!,NSE:TORNTPHARM1!,NSE:TORNTPHARM1!,NSE:AUROPHARMA1!,NSE:LAURUSLABS1!,NSE:APOLLOHOSP1!,NSE:APOLLOHOSP1!
            redCloud_str = split_json_list[3].split(":", maxsplit=1)[1]
            redCloud_list = redCloud_str.split(",")
            print(redCloud_list)
            
            ############## List 5 : greenVSLRT_list:None,NSE:DIVISLAB1!,NSE:CIPLA1!,NSE:ALKEM1!,NSE:LUPIN1!,NSE:BIOCON1!,NSE:ABBOTINDIA1!,NSE:LALPATHLAB1!,NSE:SYNGENE1!
            greenVSLRT_str = split_json_list[4].split(":", maxsplit=1)[1]
            greenVSLRT_list = greenVSLRT_str.split(",")
            print(greenVSLRT_list)
            
            ############## List 6 : redVSLRT_list:None,NSE:SUNPHARMA1!,NSE:DRREDDY1!,NSE:APOLLOHOSP1!,NSE:PEL1!,NSE:TORNTPHARM1!,NSE:TORNTPHARM1!,NSE:AUROPHARMA1!,NSE:LAURUSLABS1!,NSE:APOLLOHOSP1!,NSE:APOLLOHOSP1!
            redVSLRT_str = split_json_list[5].split(":", maxsplit=1)[1]
            redVSLRT_list = redVSLRT_str.split(",")
            print(redVSLRT_list)
            
            
            current_datetime =  datetime.datetime.now()

            # Format the date and time as a string in the specified format
            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H")

            # Create the filename
            filename = getFilePath()+"Output/"+"VSLRT_{formatted_datetime}.xlsx"

            
            if os.path.exists(filename):
                df = pd.read_csv(filename)
            else :
                # read the options_lots file to get list of symbols            
                df_symbols=pd.read_csv(getFilePath()+"Symbol_list.csv")
                
                df['code'] = df_symbols['SYMBOL']
                df['code_TV'] = df_symbols['TradingView_Symbol']
                df['RegrVWAPCross'] = 0   # RegrVWAPCrossUP = 1 ; RegrVWAPCrossDN = -1
                df['GreenRedCloud'] = 0   # greenCloud = 1 ; redCloud = -1
                df['VSLRT'] = 0   # greenVSLRT = 1 ; redVSLRT = -1
                
            
            for code in RegrVWAPCrossUP_list:   
                df.loc[df['code_TV'] == code, 'RegrVWAPCross'] = 1
            
            for code in RegrVWAPCrossDN_list:
                df.loc[df['code_TV'] == code, 'RegrVWAPCross'] = -1
              
            for code in greenCloud_list:
                df.loc[df['code_TV'] == code, 'GreenRedCloud'] = 1
            
            for code in redCloud_list:
                df.loc[df['code_TV'] == code, 'GreenRedCloud'] = -1   
            
            for code in greenVSLRT_list:
                df.loc[df['code_TV'] == code, 'VSLRT'] = 1
                
            for code in redVSLRT_list:
                df.loc[df['code_TV'] == code, 'VSLRT'] = -1
                
           
            
            
            
            
            #df.to_csv(filename, index=False)
            df.to_excel(filename, index=False )

            print(f"DataFrame has been written to {filename}")
            
            #dict = json.loads(json_payload)
            ''' print(json_payload)
            print ("\n\n Dict : ")
            print (dict)
            
            df = pd.DataFrame.from_dict(dict, orient='index')
            print("\n\n DataFrame : ")
            print (df)
            print ("\n\n") '''
            
            
            
            
            # Process the payload as needed 
            # Example: Save payload data to a Django model
            # MyModel.objects.create(data=payload['some_key'])
            #print(json.dumps(payload, indent=4))
            ''' with open('webhook_data/payload.json', 'w+') as f:
                print ("in file control :" + json_payload)
                json.dump(json_payload, f, indent=4)
                f.close()    '''
            
             
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt
def webhook_lorentz(request):
    print ("webhooked lorentz")
    if request.method == 'POST':
        # Assuming the payload is sent as JSON
        print ("method post!")
        try:
            print("try block")
            req = str(request.body)
            split_json_list = req.split(";" )
            
            #initialize dataframe
            df = pd.DataFrame()  
            #df.columns = ['code', 'code_TV', 'candlesSinceLastLong', 'closeAtLastLong'  , 'candlesSinceLastShort', 'closeAtLastShort']
            
            
            ########### Generate Filename
            current_datetime =  datetime.datetime.now()

            # Format the date and time as a string in the specified format
            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H")

            # Create the filename
            filename = getFilePath()+"Output/"+"lorentz_"+ formatted_datetime + ".xlsx"
            
            if os.path.exists(filename):
                df = pd.read_excel(filename)
            else :
                # read the options_lots file to get list of symbols            
                df_symbols=pd.read_csv(getFilePath()+"Symbol_list.csv")
                df['code'] = df_symbols['SYMBOL']
                df['code_TV'] = df_symbols['TradingView_Symbol']
                
            # Populate Dataframe from JSON
            for row in split_json_list:
                #print(row + '\n')            
            
                value_list = row.split(",")
                code_tv = value_list[0].strip("'")
                candlesSinceLastLong = value_list[1]
                closeAtLastLong = value_list[2]
                candlesSinceLastShort = value_list[3]
                closeAtLastShort = value_list[4].strip("'")
                donchSignal = value_list[5].strip("'") 
                donchPrevResult = value_list[6].strip("'") 
                donchBarsBack = value_list[7]
                donchPrice = value_list[8]
                
                df.loc[df['code_TV'] == code_tv, ['candlesSinceLastLong', 'closeAtLastLong', 'candlesSinceLastShort', 'closeAtLastShort' , 'donchSignal' , 'donchPrevResult' , 'donchBarsBack' , 'donchPrice']] = [ candlesSinceLastLong , closeAtLastLong , candlesSinceLastShort , closeAtLastShort  , donchSignal , donchPrevResult , donchBarsBack , donchPrice ]
                
                
            
            #df.to_csv(filename, index=False)
            df.to_excel(filename, index=False )

            print(f"DataFrame has been written to {filename}")
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt
def webhook_lorentz_multiTimeframe(request):
    print ("webhooked lorentz multitimeframe")
    if request.method == 'POST':
        # Assuming the payload is sent as JSON
        print ("method post!")
        try:
            print("try block")
            req = str(request.body)
            split_json_list = req.split("," )    # symbol_TV:BHARTIARTL,
            
            #initialize dataframe
            df = pd.DataFrame() 
            filename = getFilePath()+"Output/lorentz_multiTimeframe.xlsx"
            df = pd.read_excel(filename )
            
            
            
            code = split_json_list[0].split(":")[1].strip("'").strip(' ')
            code = 'NSE:'+ code + '1!'
            
            LORENTZ_15 = split_json_list[1].split(":")[1].strip("'").strip(' ')
            LORENTZ_15_CANDLE	= split_json_list[2].split(":")[1].strip("'").strip(' ')
            LORENTZ_15_CLOSE	=split_json_list[3].split(":")[1].strip("'").strip(' ')
            LORENTZ_hr	= split_json_list[4].split(":")[1].strip("'").strip(' ')
            LORENTZ_hr_CANDLE = split_json_list[5].split(":")[1].strip("'").strip(' ')
            LORENTZ_hr_CLOSE	= split_json_list[6].split(":")[1].strip("'").strip(' ')
            LORENTZ_daily	= split_json_list[7].split(":")[1].strip("'").strip(' ')
            LORENTZ_daily_CANDLE	= split_json_list[8].split(":")[1].strip("'").strip(' ')
            LORENTZ_daily_CLOSE    = split_json_list[9].split(":")[1].strip("'").strip(' ')

            df.loc[df['symbol_TV'] == code , ['LORENTZ_15',	'LORENTZ_15_CANDLE' , 'LORENTZ_15_CLOSE', 'LORENTZ_hr', 'LORENTZ_hr_CANDLE', 'LORENTZ_hr_CLOSE', 'LORENTZ_daily', 'LORENTZ_daily_CANDLE',	'LORENTZ_daily_CLOSE'] ] = \
                                    [LORENTZ_15 , LORENTZ_15_CANDLE , LORENTZ_15_CLOSE , LORENTZ_hr , LORENTZ_hr_CANDLE , LORENTZ_hr_CLOSE , LORENTZ_daily , LORENTZ_daily_CANDLE , LORENTZ_daily_CLOSE ]
                                    

            
            df.to_excel(filename, index= True)
            print(f" {filename} has been updated for symbol : {code}")
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




apimgr = ApiManager()

def refresh_json(request):
    opCron = OptionsCron()
    opCron.fetchTrendLyneHeatMap()
    opCron.fetchTrendScreeners()
    niftyCron = niftytraderdata()
    niftyCron.updatebanlist()
    return HttpResponseRedirect(reverse('Index'))
    
def getFuturesOptionsMR(request):
    opstraObj = OpstraScraper()
    opstraObj.writeFuturesData()
    opstraObj.writeOptionsData()
    
    return redirect('/df')  


def load20DFuturesBU(request):
    data = {}
    return render(request , "opstraanalysis.html" , data)
    
def gen20DFuturesBU(request):
    sym_list = ""
    if request.method == 'POST':
        # Get the input field's value by its name attribute
        sym_list = request.POST['symbol_list']

    print (sym_list)
    
    opstraObj = OpstraScraper()
    opstraObj.writeFuturesAnalysisData(sym_list)
    return HttpResponseRedirect(reverse('Index'))


def completeFuturesAnalysis(request):
    opstraObj = OpstraScraper()
    opstraObj.writeCompleteFuturesAnalysisReport()
    return HttpResponseRedirect(reverse('Index'))

def gen20DOptionsOI(request):
    sym_list = ""
    if request.method == 'POST':
        # Get the input field's value by its name attribute
        sym_list = request.POST['symbol_list']

    print (sym_list)
    
    opstraObj = OpstraScraper()
    opstraObj.writeOptionOIData(sym_list)
    return HttpResponseRedirect(reverse('Index'))
    
def showDataframe(request):
    df_list = apimgr.getbuiltupDF()
    
    ''' # Convert the HTML table back to a DataFrame
    new_df_list = pd.read_html(df_list["df_master"].__str__())

    # Select the DataFrame from the list (use [0] if there's only one table)
    master_df = new_df_list[0]

    master_df.to_excel("Output/master_ranking.xlsx")
 '''

    
    return render(request,"df.html",{"dflist":df_list}) 

def showScreener(request,scrip=''):    
    # screenerdata=tl_scraper.getTrendLyneOptionScreenrs(scrip)

    # data={"data":screenerdata}
    screenerdata = apimgr.getScreenerDF(scrip)
    heatmapdata=apimgr.getHeatMapDF('')
    lotsize =0 
    stepsize=0
    # for dt in heatmapdata["data"]:
    #     if(dt["code"]==scrip):
    #         lotsize = dt["lotsize"]
    #         stepsize = dt["contract_step"]

    if(scrip !=''): 
        df_lots=pd.read_csv(getFilePath()+"options_lots.csv")
    
        lotsize = df_lots[df_lots["code"]==scrip]["lotsize"].values[0]
        stepsize = df_lots[df_lots["code"]==scrip]["contract_step"].values[0]
    
    

    return render(request,"screener.html",{"screenerdata":screenerdata,"scrip":scrip,"heatmapdata":heatmapdata,"lotsize":lotsize,"stepsize":stepsize}) 

def showHeatmap(request,sort=''):
    data_to_send=apimgr.getHeatMapDF(sort)
    data={"heatmapdf":data_to_send}
    return render(request,"heatmap.html",data) 


def showDashboard(request):
    
    data_to_send=apimgr.getIndustryHeatMap()
    return render(request,"index.html",data_to_send) 



def showTop20(request):
    price_longbuild=apimgr.getHeatMapDF("price_longbuild")
    oi_longbuild=apimgr.getHeatMapDF("oi_longbuild")
    price_shortbuild=apimgr.getHeatMapDF("price_shortbuild")
    oi_shortbuild=apimgr.getHeatMapDF("oi_shortbuild")
    vol_longbuild=apimgr.getHeatMapDF("vol_longbuild")
    vol_shortbuild=apimgr.getHeatMapDF("vol_shortbuild")

    buildups=[price_longbuild,oi_longbuild, vol_longbuild , price_shortbuild,oi_shortbuild, vol_shortbuild]
    displays=["PRICE LONG BUILD UP","OI LONG BUILD UP", "VOLUME LONG BUILD UP" ,"PRICE SHORT BUILD UP","OI SHORT BUILD UP" , "VOLUME SHORT BUILD UP"]
    
    data_to_send = {"data":buildups,"displays":displays}
    return render(request,"top20.html",data_to_send) 


def showTvTop20(request):
    price_longbuild=apimgr.getHeatMapDF("price_longbuild")
    oi_longbuild=apimgr.getHeatMapDF("oi_longbuild")
    price_shortbuild=apimgr.getHeatMapDF("price_shortbuild")
    oi_shortbuild=apimgr.getHeatMapDF("oi_shortbuild")
    vol_longbuild=apimgr.getHeatMapDF("vol_longbuild")
    vol_shortbuild=apimgr.getHeatMapDF("vol_shortbuild")

    buildups=[price_longbuild,oi_longbuild, vol_longbuild , price_shortbuild,oi_shortbuild, vol_shortbuild]
    displays=["PRICE LONG BUILD UP","OI LONG BUILD UP", "VOLUME LONG BUILD UP" ,"PRICE SHORT BUILD UP","OI SHORT BUILD UP" , "VOLUME SHORT BUILD UP"]
    
    data_to_send = {"data":buildups,"displays":displays}
    return render(request,"top20.html",data_to_send) 
