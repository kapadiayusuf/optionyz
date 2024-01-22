import json
import os
import pandas as pd
import numpy as np
# Create your views here.


class ApiManager():

    
    def find_latest_lorentz_file(self , folder_path): 

        all_files = os.listdir(folder_path)
        
        # all .xlsx files in the folder beginning with "lorentz_2024"
        lorentz_files =  [file for file in all_files if file.startswith("lorentz_2024") and file.lower().endswith(".xlsx")]

        if not lorentz_files:
            return None
        
        # Get the full paths of the filtered files
        lorentz_file_paths = [os.path.join(folder_path, file) for file in lorentz_files]

        latest_file = max(lorentz_file_paths, key=os.path.getmtime)
        return latest_file
    
    
    def find_closest_strike(self, target, strike_list):
        # Find the closest strike to the target 
        # for every item in strike_list , the lambda function is returning the absolute value of the difference 
        # between the target and the item in strike_list. Then the min function returns the item with the smallest difference
        closest_strike = min(strike_list, key=lambda x: abs(x - target))
        return closest_strike

    
    def getbuiltupDF(self):
        

        fpath=self.getFilePath()+"optionsheatmap.json"

        with open(fpath, 'r') as f:
            optionsmapdata = json.load(f)

        last_updated = optionsmapdata["last_updated"]    
        data_df = pd.DataFrame.from_dict(optionsmapdata["data"] )

        data_df.drop(columns=["lotsize","contract_step","qty_freeze","Sector","Industry","Underlying","symbol_TV","symbol_TV_1","MktCategory","Mcap","IntraSectorRank","NiftyRank"],inplace=True)
        
        df_lots=pd.read_csv(self.getFilePath()+"options_lots.csv")


        premarket_df = pd.read_csv(self.getFilePath()+"Output/premarket.csv")

         

        premarket_df.columns = [col.replace('\n', '') for col in premarket_df.columns]

        premarket_df.columns = [col.replace(' ', '') for col in premarket_df.columns]


        premarket_df.rename(columns={'SYMBOL': 'code'}, inplace=True)

       
        premarket_df['FINALQUANTITY'] = pd.to_numeric(premarket_df['FINALQUANTITY'].str.replace(',', ''), errors='coerce')


        premarket_df.sort_values(by="FINALQUANTITY",ascending=False,inplace=True)
        premarket_df["PRE_VOL_RANK"]="VR"+(premarket_df.reset_index().index+1).astype(str)


        # add TOP_PRE_VOL col   1st 20 rows will be true and rest will be false
        premarket_df['TOP_PRE_VOL']= False
        premarket_df['TOP_PRE_VOL'][:20] = True
        
       
       
       
        xlsx_file_path = self.getFilePath()+"Output/opstra_options.xlsx"
        opstra_df=pd.read_excel(xlsx_file_path)

        opstra_df.rename(columns={'ticker': 'code'}, inplace=True)
        if "Unnamed: 0" in opstra_df.columns:
            opstra_df.drop(columns=["Unnamed: 0"], inplace=True)

        

        xlsx_file_path_futures = self.getFilePath()+"Output/opstra_futures.xlsx"
        opstra_df_futures=pd.read_excel(xlsx_file_path_futures)

        opstra_df_futures.rename(columns={'ticker': 'code'}, inplace=True)
       # Identifying columns that contain 'Unnamed'
        unnamed_columns = [col for col in opstra_df_futures.columns if 'Unnamed' in col]

        # Dropping these columns
        if unnamed_columns:
            opstra_df_futures.drop(columns=unnamed_columns, inplace=True)


        xlsx_file_path_screener = self.getFilePath()+"Output/Complete_Futures_Analysis_Report.xlsx"
        opstrascreener_df=pd.read_excel(xlsx_file_path_screener)


        opstrascreener_df.rename(columns={'STOCKNAME': 'code'}, inplace=True)
        opstrascreener_df.rename(columns={'RESULT': '20D_OUTLOOK'}, inplace=True)
        opstrascreener_df=opstrascreener_df[["code","20D_OUTLOOK"]]
        if "Unnamed: 0" in opstrascreener_df.columns:
            opstrascreener_df.drop(columns=["Unnamed: 0","DATE"], inplace=True)


        
        ################## Get data from Lorentz file ##################
        folder_path = self.getFilePath()+"Output/"
        xlsx_file_path_screener = self.find_latest_lorentz_file(folder_path)

        #xlsx_file_path_screener = self.getFilePath()+"Output/lorentz.xlsx"
        lorentz_df=pd.read_excel(xlsx_file_path_screener)
        

        df_lots = df_lots[df_lots["code"].notna()]

        df_lots.drop(columns=["MktCategory","Mcap","IntraSectorRank","NiftyRank"],inplace=True)

        result_df = pd.merge(df_lots, data_df, on='code', how='outer')

        result_df = pd.merge(result_df, premarket_df, on='code', how='outer')

        # result_df = pd.merge(screener_df, result_df, on='code', how='outer')


        result_df["oi_change"] = pd.to_numeric(result_df["oi_change"])
        # result_df["oi"] = pd.to_numeric(result_df["oi"])
        result_df["current_price"] = pd.to_numeric(result_df["current_price"])
        result_df["current_change"] = pd.to_numeric(result_df["current_change"])
        result_df["current_difference"] = pd.to_numeric(result_df["current_difference"])
        result_df["oi_difference"] = pd.to_numeric(result_df["oi_difference"])
        result_df["contracts"] = pd.to_numeric(result_df["contracts"])
        result_df["contracts_change"] = pd.to_numeric(result_df["current_change"])
        result_df["contracts_difference"] = pd.to_numeric(result_df["contracts_difference"])


        ##LPR LOGIC
        sorted_df = result_df.sort_values(by="current_change", ascending=False)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Long Build Up"].copy()
        long_buildup_df["pricerank"] = "LPR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)
        long_buildup_df["LPR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)

        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'pricerank','LPR']], on='code', how='left')

        sorted_df = final_df.sort_values(by="current_change", ascending=True)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Short Build Up"].copy()
        long_buildup_df["pricerank"] = "SPR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)
        long_buildup_df["SPR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)

        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'pricerank',"SPR"]], on='code', how='left')

        sorted_df = final_df.sort_values(by="oi_change", ascending=False)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Long Build Up"].copy()
        long_buildup_df["oi_rank"] = "LOR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)

        long_buildup_df["LOR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)
        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'oi_rank',"LOR"]], on='code', how='left')

        sorted_df = final_df.sort_values(by="oi_change", ascending=False)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Short Build Up"].copy()
        long_buildup_df["oi_rank"] = "SOR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)
        long_buildup_df["SOR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)
        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'oi_rank','SOR']], on='code', how='left')


        sorted_df = final_df.sort_values(by="contracts_change", ascending=False)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Long Build Up"].copy()
        long_buildup_df["vol_rank"] = "LVR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)
        long_buildup_df["LVR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)
        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'vol_rank','LVR']], on='code', how='left')


        sorted_df = final_df.sort_values(by="contracts_change", ascending=True)
        long_buildup_df = sorted_df[sorted_df["builtup_str"] == "Short Build Up"].copy()
        long_buildup_df["vol_rank"] = "SVR" + (long_buildup_df.reset_index(drop=True).index + 1).astype(str)
        long_buildup_df["SVR"] = (long_buildup_df.reset_index(drop=True).index + 1).astype(int)
        final_df = pd.merge(sorted_df, long_buildup_df[['code', 'vol_rank','SVR']], on='code', how='left')


        # Assuming final_df is your DataFrame with pricerank_x, pricerank_y, oi_rank_x, and oi_rank_y columns
        # Merge pricerank_x and pricerank_y into price_rank
        final_df['price_rank'] = final_df['pricerank_x'].combine_first(final_df['pricerank_y'])

        # Merge oi_rank_x and oi_rank_y into oi_rank
        final_df['oi_rank'] = final_df['oi_rank_x'].combine_first(final_df['oi_rank_y'])

        final_df['vol_rank'] = final_df['vol_rank_x'].combine_first(final_df['vol_rank_y'])

        # Optionally, drop the original columns if they are no longer needed
        final_df.drop(columns=['pricerank_x', 'pricerank_y', 'oi_rank_x', 'oi_rank_y','vol_rank_x','vol_rank_y'], inplace=True)

        final_df["steam"] = (final_df["LPR"] - final_df["LOR"]) > 5

        final_df["TOP_OI"] = ((final_df["LOR"]  <= 20) | (final_df["SOR"]  <= 20))

        final_df["TOP_PRICE"] = ((final_df["LPR"]  <= 20) | (final_df["SPR"]  <= 20)) 

        final_df["TOP_VOL"] = ((final_df["LVR"]  <= 20) | (final_df["SVR"]  <= 20)) 

        final_df = pd.merge(final_df, opstra_df, on='code', how='outer')
        

        final_df["high_ivp"] = ((final_df["ivpq"]  >= 80)) 
        final_df["result_available"] = ~final_df["resultdate"].isna()

        final_df = pd.merge(final_df, opstrascreener_df, on='code', how='outer')

        final_df = pd.merge(final_df, opstra_df_futures, on='code', how='outer')

        final_df = pd.merge(final_df, lorentz_df, on='code', how='outer')

        

        final_df["atm"]=final_df["current_price"]-final_df["current_price"]%final_df["contract_step"]
        final_df["citm1"]=final_df["atm"]-1*final_df["contract_step"]
        final_df["citm2"]=final_df["atm"]-2*final_df["contract_step"]
        final_df["citm3"]=final_df["atm"]-3*final_df["contract_step"]
        final_df["citm4"]=final_df["atm"]-4*final_df["contract_step"]
        final_df["pitm1"]=final_df["atm"]+1*final_df["contract_step"]
        final_df["pitm2"]=final_df["atm"]+2*final_df["contract_step"]
        final_df["pitm3"]=final_df["atm"]+3*final_df["contract_step"]
        final_df["pitm4"]=final_df["atm"]+4*final_df["contract_step"]

        # update Donchian Price to match nearest strike prices
        final_df = final_df.fillna(0) 
        final_df['donchPrice'] = final_df['donchPrice'].apply(pd.to_numeric, errors='coerce')
        final_df['donchPrice'] = final_df['donchPrice'] - (final_df['donchPrice'] % final_df['contract_step'])
        
        
        # Create a new DataFrame with a column 'strikes' containing lists
        #strikes_list = pd.DataFrame({'strikes': final_df.apply(lambda row: [row['atm'] + row['contract_size'] * x for x in range(-5, 5)], axis=1)})
        #final_df['donchPrice'] = final_df.apply(lambda row: self.find_closest_strike(row['donchPrice'], row['strikes_list']), axis=1)

        
        
        conditions = [
        final_df['mediumtermoutlook'].isna(),  # Check for NaN
        final_df['mediumtermoutlook'].isin(["Short Covering", "Long Buildup", "Significant Long Buildup", "Significant Short Covering"])  # Check for specific values
        ]

        choices = [
            "BEARISH",  # Value if NaN
            "BULLISH"  # Value if one of the specific strings
        ]


        final_df['MED_OUTLOOK'] = np.select(conditions, choices, default="BEARISH")


        conditions2 = [
        final_df['shorttermoutlook'].isna(),  # Check for NaN
        final_df['shorttermoutlook'].isin(["Short Covering", "Long Buildup", "Significant Long Buildup", "Significant Short Covering"])  # Check for specific values
        ]

        final_df['SHORT_OUTLOOK'] = np.select(conditions2, choices, default="BEARISH")


        

        final_df["BUILDUP_SIG"] = (final_df['mediumtermoutlook'].isin(["Significant Long Buildup", "Significant Long Unwinding", "Significant Short Buildup", "Significant Short Covering"])) 



        conditions4 = [
            (final_df['20D_OUTLOOK'] == "BULLISH") & (final_df['MED_OUTLOOK'] == "BULLISH"),
            (final_df['20D_OUTLOOK'] == "BEARISH") & (final_df['MED_OUTLOOK'] == "BEARISH")
        ]
                

        # Define the choices corresponding to each condition
        choices4 = [
            "BULLISH_ALIGNMENT",
            "BEARISH_ALIGNMENT"
        ]

        # Apply the conditions and choices
        final_df['20D_MED_ALIGN'] = np.select(conditions4, choices4, default="na")



        conditions5 = [
            (final_df['20D_OUTLOOK'] == "BULLISH") & (final_df['SHORT_OUTLOOK'] == "BULLISH"),
            (final_df['20D_OUTLOOK'] == "BEARISH") & (final_df['SHORT_OUTLOOK'] == "BEARISH")
        ]
                

        # Define the choices corresponding to each condition
        choices5 = [
            "BULLISH_ALIGNMENT",
            "BEARISH_ALIGNMENT"
        ]

        # Apply the conditions and choices
        final_df['20D_SHORT_ALIGN'] = np.select(conditions5, choices5, default="na")


        conditions6 = [
            (final_df['candlesSinceLastShort'] - final_df['candlesSinceLastLong'] >0 ),
            (final_df['candlesSinceLastShort'] - final_df['candlesSinceLastLong'] <0 ),
        ]
                

        # Define the choices corresponding to each condition
        choices6 = [
            "BULLISH",
            "BEARISH"
        ]

        final_df['LORENTZ_SIGNAL'] = np.select(conditions6, choices6, default="na")   



        conditions7 = [
            (final_df['LORENTZ_SIGNAL'] == "BULLISH") ,
            (final_df['LORENTZ_SIGNAL'] == "BEARISH")
        ]
                

        # Replace NaN or infinite values in the relevant columns
        final_df['candlesSinceLastLong'] = final_df['candlesSinceLastLong'].replace([np.inf, -np.inf], np.nan)
        final_df['candlesSinceLastShort'] = final_df['candlesSinceLastShort'].replace([np.inf, -np.inf], np.nan)

        # You can fill NaN values with 0 or another default value
        final_df['candlesSinceLastLong'].fillna(0, inplace=True)
        final_df['candlesSinceLastShort'].fillna(0, inplace=True)


        # Define the choices corresponding to each condition
        choices7 = [
            1+(final_df["candlesSinceLastLong"]/6).astype(int),
            1+(final_df["candlesSinceLastShort"]/6).astype(int)
        ]

        # Apply the conditions and choices
        final_df['LORZENTZ_CANDLE'] = np.select(conditions7, choices7, default=0)



        # Replace NaN or infinite values in the relevant columns
        final_df['closeAtLastLong'] = final_df['closeAtLastLong'].replace([np.inf, -np.inf], np.nan)
        final_df['closeAtLastShort'] = final_df['closeAtLastShort'].replace([np.inf, -np.inf], np.nan)

        # You can fill NaN values with 0 or another default value
        final_df['closeAtLastLong'].fillna(0, inplace=True)
        final_df['closeAtLastShort'].fillna(0, inplace=True)


        # Define the choices corresponding to each condition
        choices8 = [
            1+(final_df["closeAtLastLong"]/6).astype(int),
            1+(final_df["closeAtLastShort"]/6).astype(int)
        ]

        # Apply the conditions and choices
        final_df['LORZENTZ_CLOSE'] = np.select(conditions7, choices8, default=0)


        final_df["LORZENTZ_NEW"] = ((final_df['LORZENTZ_CANDLE'] == 1) | 
                            (final_df['LORZENTZ_CANDLE'] == 2) | 
                            (final_df['LORZENTZ_CANDLE'] == 3))

        #final_df.sort_values(by="FINALQUANTITY",ascending=False,inplace=True)
        
        
        ########### Incorporating BAN status #########
        xlsx_file_path_banlist = self.getFilePath()+"Output/ban-list.xlsx"
        df_banlist = pd.read_excel(xlsx_file_path_banlist)

        df_banlist.rename(columns={'symbol_name': 'code'}, inplace=True)
       
        
        final_df = pd.merge(final_df, df_banlist[['code' ,'current_percent' , 'previous_percent' ,'BAN_STATUS']], on='code', how='left')


        final_df.to_excel(self.getFilePath()+"Output/finaldf.xlsx")


        return {"df_master":final_df.to_html()}

    def getFilePath(self):
        # if("E:" in os.getcwd()):
        #     #return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
        #     #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
        #     return "/optionstrader/webapp/utils/"
        # else:
        #     return "/var/www/optionstrader/webapp/utils/"
        return "C://django_projects/code/optionstrader/webapp/utils/"

    def getIndustryHeatMap(self):
        df= self.getHeatMapDF('','',True)
        data_industry=df.groupby(['Sector'], group_keys=False).apply(lambda grp: list(grp.value_counts().index)).to_dict()
        return {"data":data_industry}

    def getScreenerDF(self,scrip='',getDf=False):
        fpath= self.getFilePath()+"options_screener.json"
        optionsscreenerdata={}
        with open(fpath, 'r') as f:
            optionsscreenerdata = json.load(f)

        last_updated = optionsscreenerdata["last_updated"]    
        data_df = pd.DataFrame.from_dict(optionsscreenerdata["data"] )
        if(scrip != ''):
            data_df=data_df[data_df["name"]==scrip]

        data_df = data_df.sort_values(by=["type","strike"],ascending=True)   
        # if(industry==True):
        #     data_industry=(dict(data_df.groupby('Industry').apply(list)))
        #     data_to_send={"last_updated":last_updated,"data":data_industry}
        # else:
        data=data_df.to_dict("records") 
        if(getDf):
            return data_df
        else:    
            data_to_send={"last_updated":last_updated,"data":data_df.to_dict("records")}
        
        return data_to_send

    def getHeatMapDF(self,sort='',scrip='',getDf=False):
        screener_df=self.getScreenerDF('',True)

        fpath=self.getFilePath()+"optionsheatmap.json"

        with open(fpath, 'r') as f:
            optionsmapdata = json.load(f)

        last_updated = optionsmapdata["last_updated"]    
        data_df = pd.DataFrame.from_dict(optionsmapdata["data"] )
        #data_df['screener_count'] = data_df["code"].isin(screener_df["name"])
        data_df['screener_count']=data_df['code'].map(screener_df['name'].value_counts())

        # ###new code for rankin
        df_price_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="current_change",ascending=False)
        df_price_longbuild["price_rank"]="LPR"+(df_price_longbuild.reset_index().index+1).astype(str)
       
        df_oi_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="oi_change",ascending=False)
        df_oi_longbuild["oi_rank"]="LOR"+(df_oi_longbuild.reset_index().index+1).astype(str)
       
        df_vol_longbuild = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="contracts_change",ascending=False)
        df_vol_longbuild["vol_rank"]="LVR"+(df_vol_longbuild.reset_index().index+1).astype(str)
       
        df_price_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="current_change",ascending=True)
        df_price_shortbuild["price_rank"]="SPR"+(df_price_shortbuild.reset_index().index+1).astype(str)
        data_df_oi_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="oi_change",ascending=False)
        data_df_oi_shortbuild["oi_rank"]="SOR"+(data_df_oi_shortbuild.reset_index().index+1).astype(str)

        df_vol_shortbuild = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="contracts_change",ascending=True)
        df_vol_shortbuild["vol_rank"]="SVR"+(df_vol_shortbuild.reset_index().index+1).astype(str)
        
        
        
        #df_master=pd.concat([df_price_longbuild,df_oi_longbuild], axis=0, ignore_index=True,join='outer')
        df_master_long = pd.merge(pd.merge(df_oi_longbuild,df_price_longbuild) ,df_vol_longbuild)
        df_master_short = pd.merge(  df_price_shortbuild.merge(data_df_oi_shortbuild, how='inner')  , df_vol_shortbuild)
        df_master=pd.concat([df_master_long,df_master_short], axis=0, ignore_index=True)
        data_df=df_master
        # ##new code for rankin
        if(sort != ''):
            if(sort=='oi_change'):
                data_df = data_df.sort_values(by=sort,ascending=False)
            elif(sort=="price_longbuild"):
                data_df = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="current_change",ascending=False)
            elif(sort=="oi_longbuild"):
                data_df = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="oi_change",ascending=False)
            elif(sort=="price_shortbuild"):
                data_df = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="current_change",ascending=True)
            elif(sort=="oi_shortbuild"):
                data_df = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="oi_change",ascending=False)
            elif(sort=="vol_longbuild"):
                data_df = data_df[data_df["builtup_str"]=="Long Build Up"].sort_values(by="contracts_change",ascending=False)
            elif(sort=="vol_shortbuild"):
                data_df = data_df[data_df["builtup_str"]=="Short Build Up"].sort_values(by="contracts_change",ascending=True)
            else:
                data_df = data_df.sort_values(by=sort,ascending=True)    

        if(scrip!=''):
            data_df=data_df[data_df["code"]==scrip]
        if(getDf):
            return data_df
        else:
            data_to_send={"last_updated":last_updated,"data":data_df.to_dict("records")}

            return data_to_send