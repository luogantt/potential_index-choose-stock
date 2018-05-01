# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:45:01 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:26:31 2017

@author: Administrator
"""

import pymongo
import pandas

import pandas as pd
import matplotlib.pyplot as plt  
import numpy as np 
import pylab as pl
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

from matplotlib.pylab import date2num
import potential

import talib

def some_district_information(ct,rl,lk):
    
    
    tt=pandas.Timestamp('2015-01-01')

    

    query = {"city":ct,"region":rl,"district_name":lk,'weekend':{"$gt":tt}}
    fields1 = {"city":1,"region":1, "district_name":1,
               'calc_value':1,'calc_value':1,'weekend':1}

    return potential.findHouse(query,fields1)



def potential_index(dd1):
    
    dd2=dd1[['calc_value','weekend']]
    d=[int(i.strftime('%Y%m%d')) for i in dd2['weekend'] ]
    
    dtime=[(i.strftime('%Y-%m-%d')) for i in dd2['weekend'] ]
    
    dd2['ymd']=d
    
    dd2['ym']=dd2['ymd']//100
    dd2['dtime']=dtime
    
    d1=list(set(dd2['ym']))
    
    d1.sort()
    
    
    def candle(p,i):
        
        sh=p.shape[0]
        if sh>0:
            dic =  [p.iloc[0]['calc_value'], 
                   p['calc_value'].max(),
                   p.iloc[-1]['calc_value'],
                   p['calc_value'].min(),
                   p.iloc[0]['dtime']]
            return dic
            
    
    def normalize(d1,dd2):
        
        ss=[]
        for i in d1:
            #print('i=',i)
            p=dd2[dd2['ym']==i]
            p1=p.sort_values(by='ymd',ascending=True)
            ss.append(candle(p1,i))
            
        dcc=pandas.DataFrame(ss,columns=['open','high','close','low','date'])
        dcc.index=dcc['date']
        return dcc
        
    
    dcc=normalize(d1,dd2)

    df=dcc
    
    
    """
    #以下代码为绘制某小区的k线图
    hist_data=df 
    # 创建子图
    fig = plt.figure(figsize=(10, 6))
    #ax1 = plt.subplot2grid((10,4),(0,0),rowspan=5,colspan=4)
    fig, ax = plt.subplots()
    
    fig.subplots_adjust(bottom=0.2)
    # 设置X轴刻度为日期时间
    ax.xaxis_date()
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(lk)
    plt.xlabel("时间")
    plt.ylabel("股价（元）")
    #candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='g')
    plt.grid()
    
    hist_data=df .sort_index()
    # 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
    data_list = []
    for dates,row in hist_data.iterrows():
        # 将时间转换为数字
        date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
        t = date2num(date_time)
        open,high,close,low = row[:4]
        datas = (t,open,high,low,close)
        data_list.append(datas)
    
    
    
    mondays = WeekdayLocator(MONDAY)            # 主要刻度
    alldays = DayLocator()                      # 次要刻度
    #weekFormatter = DateFormatter('%b %d')     # 如：Jan 12
    mondayFormatter = DateFormatter('%m-%d-%Y') # 如：2-29-2015
    dayFormatter = DateFormatter('%d')          # 如：12
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    candlestick_ohlc(ax,data_list,width=5,colorup='r',colordown='g') 
    
    """
    
    
    
    df=dcc.drop(['date'],axis=1)*1.0
    
    df.index=list(range(df.shape[0]))
    
    #df[df['volume']==0]=np.nan
    
    #print('df=',df)
    
    """
    def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
        ewma12 = pd.ewma(price,span=fastperiod)
        ewma60 = pd.ewma(price,span=slowperiod)
        dif = ewma12-ewma60
        dea = pd.ewma(dif,span=signalperiod)
        bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,bar
    """
    
    #print(df['close'].values)
    
    macd, signal, hist = talib.MACD(df['close'].values, fastperiod=6, slowperiod=12, signalperiod=9)
    
    """
    #mydif,mydea,mybar = myMACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    
    fig = plt.figure(figsize=[10,5])
    plt.plot(df.index,macd,label='macd dif')
    plt.plot(df.index,signal,label='signal dea')
    plt.plot(df.index,hist,label='hist bar')
    #plt.plot(df.index,mydea,label='my dea')
    #plt.plot(df.index,mybar,label='my bar')
    plt.legend(loc='best')
    """
    close = [float(x) for x in df['close']]
    
    def macscore( hist):
        
        span=len(macd)-1
    
        h1=hist[span]
        if  h1>0:
            return 1
        else:
            return 0
        
    
        
    
    def RSI(df):
        
        df['RSI']=talib.RSI(np.array(close), timeperiod=12) 
        aa=list(df['RSI'])
        
        b=aa[::-1]
        #print(b)
        if b[0]>50:
            return 0
        else:
            return 1
    
    def monment(df):
        df['MOM']=talib.MOM(np.array(close), timeperiod=5)
        aa=list(df['MOM'])
        b=aa[::-1]
        if b[0]>0:
            return 1
        else:
            return 0
    
    
    
    def polyfit(close,k,pl):
        
        near_six=close[len(close)-pl:len(close)]
        xlist=list(range(pl))
        bbz1 = np.polyfit(xlist, near_six,k)
        # 生成多项式对象{
        bbp1 = np.poly1d(bbz1)
        f5=bbp1(pl-1)
        f6=bbp1(pl)
        if f6>f5:
            return 1
        else:
            return 0
        
    score=2*RSI(df)+2*monment(df)+3*polyfit(close,1,2)+2*polyfit(close,1,3)+1*polyfit(close,1,4)+2*polyfit(close,3,5)+2*macscore( hist)

    poindex=score/14
    vv=int(poindex*100)
    return vv*1.0


def city_list():

    city = db136.server_area
    #seawater.find_one()

    pos= city.find({"display":{"$ne":"全国"}},
                       {"display":1,"city_grade":1,"_id":1}).sort([("city_grade",1),("_id",1)])
    data=pandas.DataFrame(list(pos))
    #print(data)
    return data['display']
    




def region_list(city):
    #client = pymongo.MongoClient('192.168.0.136',27017) 
    #db = client.fangjia
    region = db136.region_block
    #seawater.find_one()
    query = {"city":city,"category":"region"}
    fields1 = {"name":1}
    pos = list(region.find(query,fields1))
        
    
    data=pandas.DataFrame(pos)
    return data['name']

def region_district_list(ct,rl):
    #import pandas
    #client1 = pymongo.MongoClient('192.168.0.136',27017)
    #db1 = client1.fangjia
    #seaweed1 = db1.seaweed
    
    query1 = {"status":0,"cat":"district","city":ct,"region":rl}
    fields1 = {"lat2":1,"lng2":1, "city":1,"region":1,
               "cat":1,"name":1,'estate_type2':1,'alias':1}
    
    lf=potential.find_seaweed(query1,fields1)
    return lf


#########################################################
#########################################################
#########################################################

ip='192.168.0.136'
client136 = pymongo.MongoClient(ip,27017)
db136 = client136.fangjia
cit=city_list()


date=201712
#timm=datetime.datetime.now()
db1 = client136.fangjia_stat
stat = db1.potential_index2
#########################################################
#########################################################
#########################################################

for ct in cit[0:]:
    
    #ppr=15
    
    region=region_list(ct)#[ppr:ppr+1]
    
    for rl in region:

        lf=region_district_list(ct,rl)
        
        
        
        if lf.shape[0]>1:
            
        
            for lk in lf['name']:
                
                dd1=some_district_information(ct,rl,lk)
                
                #print(dd1)
                
                
                if dd1.shape[0]>5:
                    
                
                    a=list(dd1['calc_value'].dropna())
                    if len(a)>20:
                        
                        mm=potential_index(dd1)
                        print(ct,rl,lk,mm)
                        timm=datetime.datetime.now()
                        '''
                        try:
                            """
                            #date=201712
                            timm=datetime.datetime.now()
                            client1 = pymongo.MongoClient('192.168.0.136',27017)
                            db1 = client1.luogan
                            stat = db1.potential_index
                            
                            stat.insert_one({"city":ct,"region":rl,"district_name":lk,
                                   "index":mm, "date":date,"time":timm})
                            """
                            stat.replace_one(
                                
                                {"city":ct,"region":rl,"district_name":lk,"date":date},
                               
                                {"city":ct,"region":rl,"district_name":lk,
                                                 "index":mm, "date":date,"time":timm},True
                                )
                            print(ct,rl,lk,mm)
                        except:
                            """
                            timm=datetime.datetime.now()
                            client1 = pymongo.MongoClient('192.168.0.136',27017)
                            db1 = client1.luogan
                            stat = db1.potential_index
                            
                            stat.insert_one({"city":ct,"region":rl,"district_name":lk,
                                   "index":mm, "date":date,"time":timm})
                            """
  
                            stat.replace_one(
                                
                                {"city":ct,"region":rl,"district_name":lk,"date":date},
                               
                                {"city":ct,"region":rl,"district_name":lk,
                                                 "index":mm, "date":date,"time":timm},True
                                )
                            print(ct,rl,lk,mm)
                        '''
                
                
        











