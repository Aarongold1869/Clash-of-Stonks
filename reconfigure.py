# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:14:32 2020

@author: Aaron Goldstein
"""

from time import sleep

from tabulate import tabulate 

import pandas
from pandas import DataFrame

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

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


    
UserID = 2


def purchase_order(UserID):
    
    Stock = 'tsla'
    Shares = 3
    Cost = 1600.00
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
    update_equity(UserID)
    
    
def sale_order(UserID):
    
    Stock = 'tsla'
    Shares = -10
    Cost = 1600
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
    mycursor.execute("SELECT stock FROM Portfolio")
    for x in mycursor:
        Stock_List.append(x[0])
    Stock_List = list(dict.fromkeys(Stock_List))
    
    for Stock in Stock_List:
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
        
    mycursor.execute("SELECT SUM(shares) FROM Orders WHERE Stock = '{}'".format(Stock))
    for x in mycursor:
        Total_Shares = x[0]
    
    return Total_Shares
    

def sum_col(Select, Table, Column, Value, UserID):
        
    mycursor.execute("SELECT SUM({}) FROM {} WHERE {} = '{}' AND UserID = {}".format(Select, Table, Column, Value, UserID))
    for x in mycursor:
        sum_col = x[0]
    
    return sum_col


def user_share_count(Stock, UserID):
    
    mycursor.execute("SELECT SUM(shares) FROM Orders WHERE Stock = '{}' AND UserID = {}".format(Stock, UserID))
    for x in mycursor:
        Total_Shares = x[0]
    
    return Total_Shares


def update_portfolio(UserID):
    
    Date_Time = date_time()
    
    Stock_List = []
    mycursor.execute("SELECT stock FROM Orders WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Stock_List.append(x[0])
    Stock_List = list(dict.fromkeys(Stock_List))
    
    for Stock in Stock_List:
        Shares = sum_col('shares', 'Orders', 'stock', Stock, UserID)
        Total_Cost = sum_col("investment", 'Orders', 'stock', Stock, UserID)

        mycursor.execute("SELECT * FROM Portfolio WHERE Stock = '{}' AND UserID = {}".format(Stock, UserID))
        row_count = mycursor.rowcount
        
        if row_count == 0:
            Stock_Info = [UserID, Stock, Shares, Total_Cost, Date_Time]
            Q1 = ("INSERT INTO Portfolio (UserID, stock, shares, total_cost, date_time) VALUES(%s,%s,%s,%s,%s)")
            mycursor.execute(Q1, Stock_Info)
            db.commit()
        
        else:
            mycursor.execute("UPDATE Portfolio SET shares = {}, total_cost = {}, date_time = '{}' WHERE stock = '{}' AND UserID = {}".format(Shares, Total_Cost, Date_Time, Stock, UserID))
            db.commit()

        remove_stock(Stock)
        
        
def remove_stock(Stock):
    
    mycursor.execute("SELECT SUM(shares) FROM Portfolio WHERE Stock = '{}'".format(Stock))
    for x in mycursor:
        Total_Shares = x
    
    if Total_Shares == 0:
        mycursor.execute("SET SQL_SAFE_UPDATES = 0")
        mycursor.execute("DELETE FROM Portfolio WHERE stock = '{}'".format(Stock))
        mycursor.execute("SET SQL_SAFE_UPDATES = 1")
        db.commit()


def refresh():
     
    update_stocks()
    
    Users = []
    mycursor.execute("SELECT UserID FROM User")
    for x in mycursor:
        Users.append(x[0])
        
    for UserID in Users:
        update_equity(UserID)


def update_equity(UserID):
    
    Equity = 0
    Date_Time = date_time() 
    
    mycursor.execute("SELECT cash FROM User WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Cash = x[0]
    
    mycursor.execute("SELECT (shares * price) FROM Portfolio INNER JOIN Stocks ON Portfolio.stock = Stocks.stock WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Equity = Equity + x[0]
       
    Equity_Data = [UserID, Equity, Cash, Date_Time]
    Q1 = "INSERT INTO Equity (UserID, equity, cash, date_time) VALUES (%s,%s,%s,%s)"
    mycursor.execute(Q1, Equity_Data)
    db.commit()
    
    
def show_table(UserID):    
    
    Table_Data = []
    mycursor.execute("SELECT Portfolio.stock, shares, total_cost, avg_cost_per, price FROM Portfolio INNER JOIN Stocks ON Portfolio.stock = Stocks.stock WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Stock = x[0]
        Shares = x[1]
        if not Shares:
            continue 
        
        Total_Cost = float(x[2])
        Avg_Cost = float(x[3])
        Market = float(x[4])
        Equity = float(Shares * Market)
        Profit = float(Equity - Total_Cost)
        Return = float(((Equity / Total_Cost) - 1) * 100)
        
        Record = [Stock, Shares, "${:0.2f}".format(Total_Cost),"${:0.2f}".format(Avg_Cost), "${:0.2f}".format(Equity), "${:0.2f}".format(Profit), "{:0.4f}%".format(Return)]
        Table_Data.append(Record)
    
    if not Table_Data:
        print("No stock data yet.")    
    else:
        table = tabulate(Table_Data, headers=['Stock', 'Shares', 'Total Cost', 'Average Cost', 'Equity', 'Profit', '% return'], tablefmt='orgtbl')
        print(table,"\n")
 
    
def show_balance(UserID):
    
    Initial = 200000.00
    mycursor.execute("SELECT Balance FROM Equity WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Balance = float(x[0])
        
    Profit = float(Balance - Initial)
    Return = float(((Balance / Initial)- 1) * 100)
    print("\nCurrent Balance: ${:0.2f}\nTotal Profit/Loss: ${:0.2f}\nTotal Pecent Return: {:0.4f}%\n".format(Balance, Profit, Return))
    

def show_graph(UserID):
    
    Graph_Data = []
    mycursor.execute("SELECT date_time, Balance FROM Equity WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Graph_Data.append(x)
        
    df = DataFrame (Graph_Data,columns=['Date','Balance'])
    df['Balance'] = df['Balance'].astype(float)
    df.plot(x = 'Date', y = 'Balance')

    plt.show()

    
def view_portfolio(UserID):
    
    refresh()
    show_table(UserID)
    show_balance(UserID)
    show_graph(UserID)
    
    
    
    
def day():

    Now = datetime.now()
    Date = Now.strftime("%m/%d/%Y")
    Min = Date + " 08:30:00"
    Max = Date + " 16:00:00"
    
   
    Min = datetime.strptime(Min, '%m/%d/%Y %H:%M:%S')
    Max = datetime.strptime(Max, '%m/%d/%Y %H:%M:%S')
    
    
    return Min, Max
    
# def week():
    
# def month():

# def 3month():
    
# def year():
    
# def 5year():
    
def graph_test():
    
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    week = mdates.WeekdayLocator()
    hour = mdates.HourLocator()
    minute = mdates.MinuteLocator()
    
    years_fmt = mdates.DateFormatter('%Y')
    
    Range = day()
    Min = Range[0]
    Max = Range[1]
    
    
    data = []
    mycursor.execute("SELECT date_time, Balance FROM Equity WHERE UserID = {}".format(UserID))
    for x in mycursor:
        data.append(x)
    
    df = DataFrame (data,columns=['Date','Balance'])
    df['Balance'] = df['Balance'].astype(float)
    df.plot(x = 'Date', y = 'Balance')
    # fig, df = plt.subplots()
    # fig.autofmt_xdate()
    df.set_xlim([datetime.date(Min), datetime.date(Max)])
    # df.set_ylim([0, 5])
    plt.show()
    
    # format the ticks
    # df.xaxis.set_major_locator(years)
    # df.xaxis.set_major_formatter(years_fmt)
    # df.xaxis.set_minor_locator(months)
    
    # ## round to nearest years.
    # # datemin = np.datetime64(data['Date'][0], 'Y')
    # # datemax = np.datetime64(data['Date'][1], 'Y') + np.timedelta64(1, 'Y')
    # # df.set_xlim(datemin, datemax)
    
    # # format the coords message box
    # df.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    # df.format_ydata = lambda x: '$%1.2f' % x  # format the price.
    # df.grid(True)
    
    # # rotates and right aligns the x labels, and moves the bottom of the
    # # axes up to make room for them
    # fig.autofmt_xdate()
    
    # plt.show()




# day()
# test()
# purchase_order(UserID)
view_portfolio(UserID)
# table_data(UserID)
# refresh()
# update_portfolio(UserID)
# stock_update()
