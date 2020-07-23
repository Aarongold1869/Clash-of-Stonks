# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:14:32 2020

@author: Aaron Goldstein
"""

import requests
import alpha_vantage
## Alpha_Vantage API Key
API_KEY = 'GFUV3575DL68NYGL'
    
## command imports data from AV API and uses Python Pandas to format data
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(API_KEY, output_format = 'pandas')

from datetime import datetime

import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "stonkdb"
    )

mycursor = db.cursor(buffered=True)


def API_call(Stock):

    while True:
        
        try:
            values_1, columns = ts.get_intraday(symbol = Stock)
            return values_1
        
        except ValueError:
            continue

def date_time():
    
    Now = datetime.now()
    Date_Time = Now.strftime("%Y/%m/%d %H:%M:%S")
    
    return Date_Time


UserID = 1


def purchase_order(UserID):
    
    Stock = 'amd'
    Shares = 20
    Cost = 269.69
    Investment = (Shares * Cost)
    Date_Time = date_time()
    
    Order = [UserID, Stock, Shares, Cost, Date_Time]
    
    Get_Cash = "SELECT cash FROM User WHERE UserID = {}".format(UserID)
    mycursor.execute(Get_Cash)
    for x in mycursor:
        Cash = float(x[0])
    Cash = (Cash - Investment)
    
    submit_order(Order)
    update_cash(Cash)
    update_portfolio(UserID)
    
    
def sale_order(UserID):
    
    Stock = 'amd'
    Shares = -200000
    Cost = 59
    Investment = (Shares * Cost)
    Date_Time = date_time()
    
    Order = [UserID, Stock, Shares, Cost, Date_Time]
    
    Get_Cash = "SELECT cash FROM User WHERE UserID = {}".format(UserID)
    mycursor.execute(Get_Cash)
    for x in mycursor:
        Cash = float(x[0])
    Cash = (Cash - Investment)
    
    submit_order(Order)
    update_cash(Cash)
    update_portfolio(UserID)


def submit_order(Order):
      
    Order_load = "INSERT INTO Orders (UserID, stock, shares, cost_per, date_time) VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(Order_load, Order)
    db.commit()


def update_cash(Cash):
    
    mycursor.execute("UPDATE USER SET cash = {} WHERE UserID = {}".format(Cash, UserID))    
    db.commit()
    
  
def update_stocks():
    
    Date_Time = date_time()
    
    Stock_List = []
    mycursor.execute("SELECT stock FROM Orders")
    for x in mycursor:
        Stock_List.append(x[0])
    Stock_List = list(dict.fromkeys(Stock_List))
        
    for x in Stock_List:
        Stock = x

        Total_Shares = share_count(Stock)
        if Total_Shares == 0:
            continue
        
        Data = API_call(Stock)
        Market = float(Data['4. close'][0])
        
        mycursor.execute("SELECT * FROM Stocks WHERE Stock = '{}'".format(Stock))
        row_count = mycursor.rowcount
        
        if row_count == 0:
            Stock_Info = [Stock, Market, Date_Time]
            Q1 = ("INSERT INTO Stocks (stock, price, date_time) VALUES(%s,%s,%s)")
            mycursor.execute(Q1, Stock_Info)
            db.commit()
        
        else:
            mycursor.execute("UPDATE Stocks SET price = {}, date_time = '{}' WHERE stock = '{}'".format(Market, Date_Time, Stock))
            db.commit()

        
def share_count(Stock):
        
    Total_Shares = 0
    mycursor.execute("SELECT shares FROM Orders WHERE Stock = '{}'".format(Stock))
    for x in mycursor:
        Total_Shares = Total_Shares + x[0]
    
    return Total_Shares
    

def sum_col(Select, Table, Column, Value, UserID):
        
    sum_col = 0
    mycursor.execute("SELECT {} FROM {} WHERE {} = '{}' AND UserID = {}".format(Select, Table, Column, Value, UserID))
    for x in mycursor:
        sum_col = sum_col + x[0]
    
    return sum_col


def user_share_count(Stock, UserID):
    
    Total_Shares = 0
    mycursor.execute("SELECT shares FROM Orders WHERE Stock = '{}' AND UserID = {}".format(Stock, UserID))
    for x in mycursor:
        Total_Shares = Total_Shares + x[0]
    
    return Total_Shares


def update_portfolio(UserID):
    
    Date_Time = date_time()
    
    Stock_List = []
    mycursor.execute("SELECT * FROM Orders WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Stock_List.append(x[2])
    Stock_List = list(dict.fromkeys(Stock_List))
    
    for x in Stock_List:
        Shares = sum_col('shares', 'Orders', 'stock', x, UserID)
        Total_Cost = sum_col("investment", 'Orders', 'stock', x, UserID)

        mycursor.execute("SELECT * FROM Portfolio WHERE Stock = '{}' AND UserID = {}".format(x, UserID))
        row_count = mycursor.rowcount
        
        if row_count == 0:
            Stock_Info = [UserID, x, Shares, Total_Cost, Date_Time]
            Q1 = ("INSERT INTO Portfolio (UserID, stock, shares, total_cost, date_time) VALUES(%s,%s,%s,%s,%s)")
            mycursor.execute(Q1, Stock_Info)
            db.commit()
        
        else:
            mycursor.execute("UPDATE Portfolio SET shares = {}, total_cost = {}, date_time = '{}' WHERE stock = '{}' AND UserID = {}".format(Shares, Total_Cost, Date_Time, x, UserID))
            db.commit()
    


def update_equity(UserID):
    
    Date_Time = date_time()
    
    # update_stocks()
    Date_Time = date_time()
    
    Equity = 0 
    mycursor.execute("SELECT stock FROM Portfolio WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Stock = x[0]
        print(Stock)
        
    #     mycursor.execute("SELECT shares FROM PORTFOLIO WHERE stock = '{}' AND UserID = {}".format(Stock, UserID))
    #     for x in mycursor:
    #         Shares = float(x[0])
            
    #     # mycursor.execute("SELECT price FROM Stocks WHERE stock = '{}'".format(Stock))
    #     # for x in mycursor:
    #     #     Market = float(x[0])
            
    # # Equity = (Equity + (Shares * Market))

    #         print(Shares)
        
    # Equity_Data = [UserID, Equity, Date_Time]
    # Q1 = "INSERT INTO Equity (UserID, equity, date_time) VALUES (%s,%s,%s)"
    # mycursor.execute(Q1, Equity_Data)
    # db.commit()
    
    
    

update_equity(UserID)
# sale_order(UserID)
# stock_update()
