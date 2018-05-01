# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 10:32:05 2017

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

################################
date=201712
ddd136='192.168.0.136'
################################


client136 = pymongo.MongoClient(ddd136,27017)
db136 = client136.fangjia


data=client136.fangjia_stat
potent=data.potential_index2



def city_list():
    #client = pymongo.MongoClient('192.168.0.136',27017) #'192.168.0.65',27777
    #db = client.fangjia
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

def city_index(ct,date):
    query = {"city":ct,"date":date,"index":{"$gte":50}}
    up= potent.count(query)
    
    query1 = {"city":ct,"date":date,"index":{"$lt":50}}
    
    down= potent.count(query1)
    mind=min(up,down)
    if mind>0:
        
        inde=int(100*up/(up+down))
        return inde

def region_index(ct,rl,date):
    query = {"city":ct,"region":rl,"date":date,"index":{"$gte":50}}
    up= potent.count(query)
    
    query1 = {"city":ct,"region":rl,"date":date,"index":{"$lt":50}}
    
    down= potent.count(query1)
    mind=min(up,down)
    if mind>0:
        
        inde=round(100*up/(up+down),2)
        return inde
    
cit=city_list()
db1 = client136.fangjia_stat
stat_city = db1.city_potential

stat_region = db1.region_potential

for ct in cit[0:]:  
    cde= city_index(ct,date)
    
    
    if cde!=None:
        
        print(ct,cde)
        tt=datetime.datetime.now()
        #timm=datetime.datetime.now()
        """
        stat_city.insert_one({"city":ct,
                   "city_index":cde, "date":date,"time":tt})
        """

        stat_city.replace_one(
        
            {"city":ct,"date":date},
           
            {"city":ct,"city_index":cde, "date":date,"time":tt},True
            )
        

        region=region_list(ct)#[ppr:ppr+1]
        
        for rl in region:
            red=region_index(ct,rl,date)
            #print(ct,rl,red)
            if red!=None: 
                tt=datetime.datetime.now()
                print(ct,rl,red)
                """
                stat_region.insert_one({"city":ct,"region":rl,
                           "region_index":red, "date":date,"time":tt})
                """
                
                stat_region.replace_one(
                
                    {"city":ct,"region":rl,"date":date},
                   
                    {"city":ct,"region":rl,
                           "region_index":red, "date":date,"time":tt},True
                    )                
                        

                    










