# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:05:16 2020

@author: Aaron Goldstein
"""

import requests
import alpha_vantage
## Alpha_Vantage API Key

def API_KEY():
    KEY_LIST = ['GFUV3575DL68NYGL',
               'N21LKWQI58WK97LN',
               '5R9FTZ3EY91YEH9B',
               'XPFH9QO3948RFS2S',
               '5GVJ4G1B1WDM4VK9',
               'E9XABCI5BN4QP4AU',
               'YCSEA2FAACRIFY8F',
               'ZUS6JA7XBA2Y8YVZ',
               'UGI3LMMZJYL1EKO7',
               'WECSVTT9HPR3NHZL']
     
    return KEY_LIST
    
## command imports data from AV API and uses Python Pandas to format data
from alpha_vantage.timeseries import TimeSeries

## allows operation on JSON objects and files
import json

import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "stonkdb"
    )
## iterates through MySQL data stored in tables
mycursor = db.cursor()

from time import sleep

KEY_LIST = API_KEY()
stonk_list = ['tsla',
              'ibm',
              'tgt',
              'amzn',
              'amd',
              'msft',
              'dal',
              'dis',
              'ccl',
              'aal',
              'spy',
              'f',]             

length = len(stonk_list)

i = 0
j = 0
counter = 1 


combined = []

while i < length:
   tup = (KEY_LIST[j], stonk_list[i])
   combined.append(tup)       

   i+=1
   
   if counter == 5:
       j += 1
       counter = 1
      
   if j > len(KEY_LIST):
       j = 0
       
   counter+=1
   
for x in combined:
    group = x
    
    if group[1] == '':
        break
    
    else:
        API_KEY = group[0] 
        Stonk = group[1]
        
        ts = TimeSeries(API_KEY, output_format = 'pandas')
        value, columns = ts.get_intraday(symbol = Stonk)
        value['4. close']
        #assign most recent stock value to variable 'Market' to be used in calculations 
        Market = float(value['4. close'][0])
        
        print(Market)
        
        if length > 5:
            sleep(7)
        
        
        
        
        
        
        
        
        
        
        