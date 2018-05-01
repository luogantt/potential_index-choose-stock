from potential import mongoClients as mongoClients
import time
import pandas

def get_collection(db, name, host="192.168.0.136", port=27017):
    return mongoClients.MongoClients(db, name, host, port).collection

db136="192.168.0.136"

db222='222.73.196.152'


def findHouse(query, fields=None):

    seawater105 = get_collection("fangjia", "district_stat", db136, 27017)    
    for err_count in range(0, 10):
        
        try:
            
            lt= seawater105.count(query)
            pos = list(seawater105.find(query).limit(lt))
            data=pandas.DataFrame(pos)
            del pos
            return data
        
        except :
             
            #err_count = err_count + 1
            lt= seawater105.count(query)
            pos = list(seawater105.find(query).limit(lt))
            data=pandas.DataFrame(pos)
            del pos
            return data
        






def find_seaweed(query, fields=None):
    
    #dirlt=p[0]
    
    #client1 = pymongo.MongoClient('192.168.0.136',27017)
    #db1 = client1.fangjia
    #seaweed1 = db1.seaweed 
    
    seawater105 = get_collection("fangjia", "seaweed", "192.168.0.136", 27017)    
    for err_count in range(0, 10):
        
        try:
            
            lt= seawater105.count(query)
            
            pos = list(seawater105.find(query).limit(lt))
            data=pandas.DataFrame(pos)
            del pos
            return data
        
        except :
             
            #err_count = err_count + 1
            lt= seawater105.count(query)
            pos = list(seawater105.find(query).limit(lt))
            data=pandas.DataFrame(pos)
            del pos
            return data

    raise Exception("yang ben cha xun shi bai1")
    
    
    
    
    

    

    



















         
                 
