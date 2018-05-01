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

import tushare as ts

client1 = pymongo.MongoClient('192.168.10.182',27017)
db1 = client1.stock.potential


'''        
def before_month_lastday(ti):
    from dateutil.parser import parse
    today=parse(str(ti))
    
    #first = datetime.date(day=1, month=today.month, year=today.year)
    
    lastMonth = today - datetime.timedelta(days=0)
    
    def plus(k):
        if k<10:
            return '0'+str(k)
        else:
            return str(k)
    y=lastMonth.year
    m=lastMonth.month
    d=lastMonth.day
    #day=calendar.monthrange(y,m)[1]

    cc=str(y)+plus(m)+plus(d)
    #bb=parse(cc)
    #pacific = pytz.timezone('Asia/Shanghai')
    #return pacific.localize(bb) 
    return int(cc)      
'''


def potential_index(tl):
    
    #df=ts.get_hist_data(name,start=bf,end=now)
    df=ts.get_hist_data(tl[0],start=tl[1],end=tl[2])
    
    if str(type(df))!="<class 'NoneType'>":
        
        if df.shape[0]>10:


            print('df=',df)
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
                #print(close)
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
            db1.save({'name':tl[0],'potential':vv})
            #return vv*1.0






#mm=potential_index(code[100])

'''
for name in code:
    
    
    mm=potential_index(name)
    print(name,mm)
    timm=datetime.datetime.now()

'''            
ak=ts.get_stock_basics()

code=list(ak.index)



def front_step_time(day):
    now = datetime.datetime.now()
    front = now - datetime.timedelta(days=day)
    d1 = front.strftime('%Y-%m-%d')
    #return int(d1)
    return d1

now=front_step_time(0)

bf=front_step_time(720)

sheet=pd.DataFrame()
sheet['code']=code

sheet['bf']=bf
sheet['sta']=now
#name='600354'
#b1=potential_vocanol(name,'2017-11-14','2018-02-14')
#b2=potential_vocanol(name,'2018-02-14','2018-04-13')
client1 = pymongo.MongoClient('192.168.10.182',27017)
db1 = client1.stock.potential

import time
from multiprocessing import Pool
import numpy as np

if __name__ == "__main__" :
  startTime = time.time()
  testFL =sheet.values
  #ll=code
  pool = Pool(10)#可以同时跑10个进程
  pool.map(potential_index,testFL)
  pool.close()
  pool.join()   
  endTime = time.time()
  print ("time :", endTime - startTime)









