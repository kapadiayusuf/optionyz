from django import template
import time
from datetime import date,datetime

register = template.Library()


@register.filter
def showTop20Dashboard(dict_data):

    html=''
    for i in range(len(dict_data)):
        html+='<div class="card col-2">'
        html+='<div class="card-header"><b>'+getTop20Header(i)+'</b></div>'
        html+='<div class="card_body">'
        html+='<table>'
        if(i<3):
            html+=showTop20(dict_data[i]["data"],0,"LONG")    
        else:
            html+=showTop20(dict_data[i]["data"],0,"SHORT")
        html+='</table>'
        html+='</div>'
        html+='</div>'

    html+='<div class="card col-2">'
    price_dicts=[dict_data[0],dict_data[3]]
    oi_dicts=[dict_data[1],dict_data[4]]
    vol_dicts=[dict_data[2],dict_data[5]]
    j=0
    html+='<div class="card-header"><b>TOP PRICE</b></div>'
    for i in range(len(price_dicts)):
        
        
        html+='<div class="card_body">'
        html+='<table>'
        html+=showTop20(price_dicts[i]["data"],j,i,oi_dicts)    
        html+='</table>'
        html+='</div>'
        if(len(price_dicts[i]["data"])>20):
            j = 20
        else:
            j=len(price_dicts[i]["data"])
    html+='</div>'

    html+='<div class="card col-2">'
    
    j=0
    html+='<div class="card-header"><b>TOP OI</b></div>'
    for i in range(len(oi_dicts)):
        
        
        html+='<div class="card_body">'
        html+='<table>'
        
        html+=showTop20(oi_dicts[i]["data"],j,i,price_dicts)    
        html+='</table>'
        html+='</div>'
        
        if(len(oi_dicts[i]["data"])>20):
            j = 20
        else:
            j=len(oi_dicts[i]["data"])
        
    html+='</div>'
    
    html+='<div class="card col-2">'
    j=0
    html+='<div class="card-header"><b>TOP VOLUME</b></div>'
    for i in range(len(vol_dicts)):
        
        
        html+='<div class="card_body">'
        html+='<table>'
        html+=showTop20(vol_dicts[i]["data"],j,i,price_dicts)    
        html+='</table>'
        html+='</div>'
        if(len(vol_dicts[i]["data"])>20):
            j = 20
        else:
            j=len(vol_dicts[i]["data"])
    html+='</div>'



    return html

@register.filter
def showTop20(top20_list,j=0,k="LONG",otheridct=[]):
    html=""
    rank=0

    if(k==1):
        rank=1

    showRank=False
    # long_short="LONG"
    # if(k>1):
    #  
    #    long_short="SHORT"

    if(k == 0):
        showRank=True
        k="LONG"
    if(k == 1):
        showRank=True
        k="SHORT"

    i=1
    for l in top20_list:
        scrip = l["code"]
        isvalrepeat=checkIfvalExistsINDict(scrip,otheridct)
        scrip = l["code"].replace("-","_")
        scrip = scrip.replace("&","_")
        rank_prefix="LR"
        disp_rank=(i+j)
        p_rank = l["price_rank"]
        oi_rank = l["oi_rank"]
        vol_rank = l["vol_rank"]
        if(rank==1):
            rank_prefix="SR"
            disp_rank=disp_rank-j
        if(showRank):
            #html+=str(isvalrepeat)
            tdstyle=""
            # if(isvalrepeat):
            #     tdstyle="color:#ff00ff"
            #html+="<tr class='small' style='padding:2px;'><td><span style='"+tdstyle+"'>t"+str(i+j)+" = 'NSE:"+scrip+"1!'</span>, BU"+str(i+j)+"='"+str(k)+"',RANK"+str(i+j)+"='"+rank_prefix+str(disp_rank)+ ', ' + p_rank+ ', ' + oi_rank   +"'</td></tr>"
            html+="<tr class='small' style='padding:2px;'><td><span style='"+tdstyle+"'>t"+str(i+j)+" = 'NSE:"+scrip+"1!'</span>, BU"+str(i+j)+"='"+str(k)+"',RANK"+str(i+j)+"='"+  p_rank+ ', ' + oi_rank+ ', ' + vol_rank   +"'</td></tr>"
        else:
            html+="<tr class='small'><td>t"+str(i+j)+" = 'NSE:"+scrip+"1!', BU"+str(i+j)+"='"+str(k)+"'</td></tr>"
        i+=1
        if(i>20):
            break
    return html

def checkIfvalExistsINDict(val,dict):
    try:
        for d in dict:
            for dt in d["data"]:
                if(val == dt["code"]):
                    return True
    except Exception as e:
        {}

    return False

@register.filter
def getTop20Header(index):
    displays=["PRICE LONG BUILD UP","OI LONG BUILD UP", "VOLUME LONG BUILD UP" ,"PRICE SHORT BUILD UP","OI SHORT BUILD UP" , "VOLUME SHORT BUILD UP" ]
    return displays[index]

@register.filter
def getPosNegPercent(val):
    val = round(float(val),2)
    if(val > 0):
        return "<p class='text-success'>"+str(val)+"%</p>"
    else:
        return "<p class='text-danger'>"+str(val)+"%</p>"


@register.filter
def getTimeAgo(time_to_check):
    timestamp = int(time.time()*1000.0)
    millis = timestamp - time_to_check
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    hours = int(hours)
    return str(hours)+"h" +":" +str(minutes)+"m" +":" +str(seconds) +"s ago"

@register.filter
def getTotalLen(lst):
    return len(lst)*9

@register.filter
def getStopLoss(price):
    return round(float(price) * 0.9,2)

@register.filter
def getFixedProfit(price):
    return round(float(price) * 1.2,2)

@register.filter
def getRiskRewardProfit(price):
    price=float(price)
    return round(price+(price-getStopLoss(price))*3,2)

@register.filter
def getMaxProfit(price,lotsize):
    try:
        ft= round(float(price) * 1.2,2)-float(price)
        pr=100000/(float(price)*float(lotsize))
        pr= int(round(pr,2))
        #pr=int(round(pr,2))
        
        return round(ft*lotsize*pr,2)

    except:
        pr=0    
    return 0
    
    
@register.filter
def getMaxLoss(price,lotsize):
    try:
        fl= round(float(price) * 0.1,2)
        pr=100000/(float(price)*float(lotsize))
        pr= int(round(pr,2))
        return round(fl*lotsize*pr,2)
    

    except:
        pr=0    
    return 0

    
@register.filter
def showIndustryOI(industrylist):
    # industrylist = sorted(industrylist, key=lambda x: x[4] if x[4] > 0 else x[4] ,reverse=True)
    industrylist = sorted(industrylist, key=lambda x: (x[4]>0, x[4]),reverse=True)

    html=""
    for industry in industrylist:
        if(industry != "index"):
            html+="<tr><td><a style='text-decoration:none;' href='/screeners/"+industry[0]+"'>"+industry[0]+"<a/>"
            html+="<br><span class='badge bg-primary'>"+str(industry[29])+"</span> , <span class='badge bg-primary'>"+str(industry[30])+"</span></td>"
            html+="<td>"+getProgressBar(industry[4])+"</td>"
            
            html+="</tr>"
    return html

def getProgressBar(val):
    val=round(val,2)
    barcolor="bg-danger"
    # width=(val)*300
    width=45+(abs(val)*25)
    if val >0:
        barcolor="bg-success"
        # width=val*100
        # if(val<2):
        #     width=100
            
    pbar=""
    pbar+='<div class="progress" style="font-color:#000">'
    pbar+='<div class="progress-bar '+barcolor+'" role="progressbar" style="font-color:#000000;font-size:9px;width: '+str(width)+'%;" aria-valuenow="'+str(val)+'" aria-valuemin="0" aria-valuemax="100">'+str(val)+'</div>'
    pbar+='</div>'

    return pbar

@register.filter
def getMaxExposure(price,lotsize):
    return round(100*getMaxLoss(price,lotsize)/500000,2)

@register.filter
def getMaxReward(price,lotsize):
    return round(100*getMaxProfit(price,lotsize)/500000,2)

@register.filter
def getMaxPositionSize(price,lotsize):
    try:
        pr=100000/(float(price)*float(lotsize))
        return int(round(pr,2))

    except:
        pr=0    
    return 0
@register.filter
def getProfit_RiskReward(price):
    return round(float(price) * 1.2,2)


@register.filter
def getZeroDhaSymbol(df_data):
    '''
    SBILIFE22JAN900CE

    '''

    #ticker,strike_price,option_type="Call",isWeekly=True
    isWeekly=False
    ticker= df_data["name"]
    strike_price= int(float(df_data["strike"]))
    option_type= df_data["type"]

    opt_prefix="PE"
    if(option_type=="Call"):
        opt_prefix="CE"


    date_str_weekly=["06-Jan-2022",
    "13-Jan-2022",
    "20-Jan-2022",
    "27-Jan-2022",
    "03-Feb-2022",
    "10-Feb-2022",
    "17-Feb-2022",
    "24-Feb-2022",
    "03-Mar-2022"]
    
    date_str_monthly=["22-Jan-2022","19-Feb-2022","19-Mar-2022","16-Apr-2022","21-May-2022","18-Jun-2022","16-Jul-2022","20-Aug-2022","17-Sep-2022","22-Oct-2022","19-Nov-2022","17-Dec-2022"]


    month_arr=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    date_str=date_str_weekly
    
    if(not isWeekly):
        date_str=date_str_monthly
        
    strToday = datetime.today().strftime('%Y-%m-%d')
    dateToday = datetime.strptime(strToday, '%Y-%m-%d')
   
    SYMBOL=''

    for i in range(len(date_str)):
        date_time_obj = datetime.strptime(date_str[i], '%d-%b-%Y')
        if(dateToday<=date_time_obj):
            print(date_time_obj,dateToday<=date_time_obj)
            #MM=(f"{dateToday.month:02d}")
            MM=date_time_obj.month
            YY=(date_time_obj.year-2000)
            DD=(f"{date_time_obj.day:02d}")
            SYMBOL=ticker+str(DD)+str(month_arr[MM-1])+str(strike_price)+opt_prefix
            
            break
    return SYMBOL  
   