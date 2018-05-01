# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:45:06 2017

@author: wenyan
"""

from pymongo import MongoClient


class MongoClients:

    cache = {}

    def __init__(self, db, name, host="127.0.0.0", port=27017):

        key = db + "_" + name + "_" + host + "_" + str(port)
        if key in MongoClients.cache.keys():
            self.collection = MongoClients.cache[key]
        else:
            print("init " + key)
            collection = MongoClient(host, port).get_database(db).get_collection(name)
            MongoClients.cache[key] = collection
            self.collection = MongoClients.cache[key]
    """
    def find(self, *args, **kwargs):
        return self.collection.find(*args, **kwargs)

    def find2(self, query, fields, call):

        for item in self.collection.find(query):
            call(item)
    """        
