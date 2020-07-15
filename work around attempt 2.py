# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:03:52 2020

@author: Aaron Goldstein

#########################################################################
WORK AROUND IMPOSSIBLE DUE TO NO_PROXY ON ALPHA VANTAGE SERVER
########################################################################
"""


# ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt'

# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

import requests
from bs4 import BeautifulSoup
from random import choice
import socks
import alpha_vantage
import os
from alpha_vantage.timeseries import TimeSeries

import json
from time import sleep


def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    return {'http : socks5://': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),map(lambda x:x.text, soup.findAll('td')[1::8]))))))}


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
    
# API_KEY = 'GFUV3575DL68NYGL'
# proxy = get_proxy()
# print(proxy)

# ts = TimeSeries(API_KEY, output_format = 'pandas')
# ts.set_proxy(proxy = proxy)
# value, columns = ts.get_intraday(symbol = 'DAL')
# value['4. close']

# Market = float(value['4. close'][0])
# print(Market)

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
    
    proxy = str(get_proxy())
    group = x
    
    if group[1] == '':
        break
    
    else:
        API_KEY = group[0] 
        Stonk = group[1]
 
        ts = TimeSeries(API_KEY, output_format = 'pandas')
        ts.set_proxy(proxy=proxy)
        value, columns = ts.get_intraday(symbol = Stonk)
        value['4. close']

        Market = float(value['4. close'][0])
        
        print(Market)
        print(proxy)
        
        
#         # if length > 5:
#             # sleep(12.1)