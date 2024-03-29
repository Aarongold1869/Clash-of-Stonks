# -*- coding: utf-8 -*-
"""
Created on Fri Jul 3 17:11:09 2020

@author: Aaron Goldstein
"""
import os
import sqlalchemy

# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/secret-manager/docs/overview to help keep
# secrets secret.
db_user = os.environ["root"]
db_pass = os.environ["123"]
db_name = os.environ["stonkdb"]
db_socket_dir = os.environ.get("127.0.0.1", "/cloudsql")
cloud_sql_connection_name = os.environ["august-monument-283304:us-central1:clashdb"]

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        database=db_name,  # e.g. "my-database-name"
        query={
            "unix_socket": "{}/{}".format(
                db_socket_dir,  # e.g. "/cloudsql"
                cloud_sql_connection_name)  # i.e "august-monument-283304:us-central1:clashdb"
        }
    ),
    # ... Specify additional properties here.

)



## pulls stonk data from Alpha Vantage API
import requests
import alpha_vantage
API_KEY = 'GFUV3575DL68NYGL'
    
## command imports data from AV API and uses Python Pandas to format data
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(API_KEY, output_format = 'pandas')

## allows for creation of graphs and charts based on stonk data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

## tabulate module formats specified data in print statement table
from tabulate import tabulate 
    
## module pulls date time data
from datetime import datetime

#sleep pauses program to prevent exceed API maximum call frequency
from time import sleep

## pandas dataframe module for formatting data
from pandas import DataFrame

import re

import pymysql

import mysql.connector
# db = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     passwd = "root",
#     database = "stonkdb"
#     )

db = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "123",
    database = "stonkdb"
    )

mycursor = db.cursor(buffered=True)

##############################################################################
##############################################################################

def date_time():
    
    Now = datetime.now()
    Date_Time = Now.strftime("%Y/%m/%d %H:%M:%S")
    
    return Date_Time

def API_call(Stonk):
    
    Date_Time = date_time()
    mycursor.execute("INSERT INTO api_calls (date_time) VALUES('{}')".format(Date_Time))
    db.commit()
    
    while True:
        try:
            values_1, columns = ts.get_intraday(symbol = Stonk)
            return values_1
        except ValueError:
            continue
    
 
# retrieve user input for creating user account
def user_info():    

    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    
    while True:
        DOB = input("What is your date of birth (MM/DD/YYYY)?: ")
        valid_DOB = check_DOB(DOB)
        
        if valid_DOB == False:
            print("\nplease enter a valid birthdate (with slashes).")
            continue
        else:
            DOB = datetime.strptime(DOB, "%m/%d/%Y")
        break
    
    while True:
        email = input("What is your email?: ")
        valid = check_email(email)
        if valid == 'False':
            print("\nplease enter a vaild email address.")
            continue
        break
    
    while True:
        phone = input("What is your phone?: ")
        phone = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])
        valid = check_phone(phone)
        if valid == False:
            print("\nplease enter a vaild phone number.")
            continue
        break
    
    while True:
         user_name = input("Create a user name: ")
         valid = check_user_name(user_name)
         if valid == False:
             print("user name '{}' taken.".format(user_name))
             continue
         break
    
    while True:
         password = input("Create a password: ")
         valid = check_pw(password)
         if valid == False:
             continue
         break
    
    Date_Time = date_time()
    Cash = 200000.00
    
    User_Info = [(first_name,
                  last_name,
                  DOB,
                  email,
                  phone,
                  user_name,
                  password,
                  Date_Time,
                  Cash)]
    
    user_load(User_Info)
    
    # welcome message
    Introduction = "\nHey {}! You have ${:0.2f} to invest. Let's get started!".format(user_name, Cash)
    print(Introduction)
    
    mycursor.execute("SELECT UserID FROM user WHERE user_name = '{}'".format(user_name))
    for x in mycursor:
        UserID = x[0]
    
    return UserID
    
# create user record in User table
def user_load(User_Info):

    User_Load = "INSERT INTO user (first_name, last_name, DOB, email, phone, user_name, pass_word, date_time, cash) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
    for x, user in enumerate(User_Info):
        mycursor.execute(User_Load, user)  
    db.commit()

# allow existing user to login (return UserID to main)
def login():
    
    Valid = True
    while Valid == True:
        user_name = input("Username: ")
        password = input("Password: ")
        
        mycursor.execute("SELECT UserID FROM user WHERE user_name = '{}' AND pass_word = '{}'".format(user_name,password))
        for x in mycursor:
            UserID = x[0]
    
        try:
            UserID
        
        except UnboundLocalError:
            print("incorrect username or password")
            action = input("1. try again\n2. exit\n")
            
            if action == '1':
                continue
            
            elif action == '2':
                UserID = 'false'
                return UserID
        
        else:
            print("\nHey, {}!".format(user_name))
            return UserID


# retreive purchase info from User input 
def purchase_order(UserID):                            
    
    mycursor.execute("SELECT cash FROM user WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Cash = float(x[0])
    Cash_string = "You have ${:0.2f}".format(Cash)
    print(Cash_string)
    
    Trade = True
    while Trade == True:  
        ## retreive user input, retreive stonk data, display stonk data
        Stock = input("Insert a stock ticker or type '%' to cancel: ")
        
        if Stock == '%':
            Trade = False
            Order = "false"
            return Order
        
        else:
            Data = API_call(Stock)
            Data['4. close'].plot()
            plt.show()
            print(Data)
            Price = float(Data['4. close'][0])
            
            Mkt_String = "{} is trading at ${:0.2f}. Would you like to purchase equity in {}?".format(Stock, Price, Stock)
            print(Mkt_String)
            Action = input('1. Yes\n2. No\n')
            
            Buy = True
            while Buy == True:

                if Action =='1':   
            
                    Shares = int(input("How many shares would you like to buy? Enter # of shares:\npress '0' to cancel\n"))
                    
                    if Shares != 0:
                        
                        Investment = float(Shares * Price)
                                           
                        if (Cash - Investment) > 0:
                            
                            Cash = float(Cash - Investment)
                            
                            Equity_String = "\nCongratulations! \nYou purchased {} share(s) of {}.".format(Shares,Stock)
                            Cash_String = "you have ${:0.2f} left to invest\n".format(Cash)
                            print(Equity_String, Cash_String)
                            
                            Date_Time = date_time()

                            Order = [UserID, Stock, Shares, Price, Date_Time]
                            
                            submit_order(Order)
                            update_cash(Cash, UserID)
                            update_portfolio(UserID)
                            load_stock(Stock, Price)
                            update_equity(UserID)
                            
                            return Order
                          
                        else:
                            
                            print('\nYou dont have enough money.')
                            continue
                        
                    else:
                        Buy = False
                        break
                 
                elif Action == '2':
                  
                    break
                continue
            
def sale_order(UserID):   
    
    mycursor.execute("SELECT cash FROM user WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Cash = float(x[0])
    
    Trade = True
    while Trade == True: 
        
        Stock = input("Which stock would you like to sell?\n(Insert stock ticker. Press '%' to cancel.):")
        mycursor.execute("SELECT * FROM portfolio WHERE stock = '{}' AND UserID = {}".format(Stock, UserID))
        row_count = mycursor.rowcount
        
        if Stock == '%':
            Trade = False
            Order = "false"
            return Order
        
        if row_count == 0:
            print("\nYou do not own any shares of {}".format(Stock))
            continue
            
        else:
            
            Data = API_call(Stock)
            Data['4. close']
            Price = float(Data['4. close'][0])
            Total_Shares = sum_col('shares', 'portfolio', 'stock', Stock, UserID)

            Sell = True
            while Sell == True:
               
                Shares = int(input("{} is trading at ${}. How many shares would you like to sell?\n(Type '0' to cancel.)".format(Stock, Price)))
                
                if Shares != 0: 
                    Debit = float(Shares * Price)
                    Cash = float(Cash + Debit)
                    Inventory = Total_Shares - Shares
                    
                    if Inventory >= 0:
                        print("\nCongrats! You sold {} shares of {} for a debit to your account of ${:0.2f}.\n".format(Shares, Stock, Debit))
                    
                        Shares = (Shares * (-1))
                        Date_Time = date_time()
                        
                        Order = [UserID, Stock, Shares, Price, Date_Time]
                            
                        submit_order(Order)
                        update_cash(Cash, UserID)
                        update_portfolio(UserID)
                        load_stock(Stock, Price)
                        update_equity(UserID)
              
                        return Order
                        
                    else:
                        print("\nYou cannot sell that many shares, you own {} shares of {}.".format(Total_Shares, Stock))
                        continue
                    break 
                
                else:
                    Sell = False
                    Order = "false"
                    return Order
        
        
def submit_order(Order):
      
    Order_load = "INSERT INTO orders (UserID, stock, shares, cost_per, date_time) VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(Order_load, Order)
    db.commit()

def update_portfolio(UserID):
    
    Date_Time = date_time()
    
    Stock_List = []
    mycursor.execute("SELECT stock FROM orders WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Stock_List.append(x[0])
    Stock_List = list(dict.fromkeys(Stock_List))
    
    for Stock in Stock_List:
        Shares = sum_col('shares', 'orders', 'stock', Stock, UserID)
        Total_Cost = sum_col("investment", 'orders', 'stock', Stock, UserID)

        mycursor.execute("SELECT * FROM Portfolio WHERE Stock = '{}' AND UserID = {}".format(Stock, UserID))
        row_count = mycursor.rowcount
        
        if row_count == 0:
            Stock_Info = [UserID, Stock, Shares, Total_Cost, Date_Time]
            Q1 = ("INSERT INTO portfolio (UserID, stock, shares, total_cost, date_time) VALUES(%s,%s,%s,%s,%s)")
            mycursor.execute(Q1, Stock_Info)
            db.commit()
        
        else:
            mycursor.execute("UPDATE portfolio SET shares = {}, total_cost = {}, date_time = '{}' WHERE stock = '{}' AND UserID = {}".format(Shares, Total_Cost, Date_Time, Stock, UserID))
            db.commit()

        remove_stock(Stock)
    
def update_cash(Cash, UserID):
    
    mycursor.execute("UPDATE user SET cash = {} WHERE UserID = {}".format(Cash, UserID))    
    db.commit()
        

def sum_col(Select, Table, Column, Value, UserID):
        
    mycursor.execute("SELECT SUM({}) FROM {} WHERE {} = '{}' AND UserID = {}".format(Select, Table, Column, Value, UserID))
    for x in mycursor:
        sum_col = x[0]
    
    return sum_col

def share_count(Stock):
        
    mycursor.execute("SELECT SUM(shares) FROM orders WHERE stock = '{}'".format(Stock))
    for x in mycursor:
        Total_Shares = x[0]
    
    return Total_Shares

def user_share_count(Stock, UserID):
    
    mycursor.execute("SELECT SUM(shares) FROM orders WHERE stock = '{}' AND UserID = {}".format(Stock, UserID))
    for x in mycursor:
        Total_Shares = x[0]
    
    return Total_Shares
    
def remove_stock(Stock):
    
    mycursor.execute("SELECT SUM(shares) FROM portfolio WHERE stock = '{}'".format(Stock))
    for x in mycursor:
        Total_Shares = x
    
    if Total_Shares == 0:
        mycursor.execute("SET SQL_SAFE_UPDATES = 0")
        mycursor.execute("DELETE FROM portfolio WHERE stock = '{}'".format(Stock))
        mycursor.execute("SET SQL_SAFE_UPDATES = 1")
        db.commit()


def load_stock(Stock, Price):
    
    Date_Time = date_time()

    mycursor.execute("SELECT * FROM stocks WHERE Stock = '{}'".format(Stock))
    row_count = mycursor.rowcount
   
    if row_count == 0:  
        Stock_Info = [Stock, Price, Date_Time]
        Q1 = ("INSERT INTO stocks (stock, price, date_time) VALUES(%s,%s,%s)")
        mycursor.execute(Q1, Stock_Info)
        db.commit()
    
    else:
        mycursor.execute("UPDATE stocks SET price = {}, date_time = '{}' WHERE stock = '{}'".format(Price, Date_Time, Stock))
        db.commit()
    
def update_stocks():
    
    Date_Time = date_time()
    
    Stock_List = []
    mycursor.execute("SELECT stock FROM portfolio")
    for x in mycursor:
        Stock_List.append(x[0])
    Stock_List = list(dict.fromkeys(Stock_List))
    
    for Stock in Stock_List:
        Total_Shares = share_count(Stock)
        
        if Total_Shares == 0:
            continue
        
        Data = API_call(Stock)
        Market = float(Data['4. close'][0])

        mycursor.execute("SELECT * FROM stocks WHERE stock = '{}'".format(Stock))
        row_count = mycursor.rowcount
        
        if row_count == 0:
            Stock_Info = [Stock, Market, Date_Time]
            Q1 = ("INSERT INTO stocks (stock, price, date_time) VALUES(%s,%s,%s)")
            mycursor.execute(Q1, Stock_Info)
            db.commit()
        
        else:
            mycursor.execute("UPDATE stocks SET price = {}, date_time = '{}' WHERE stock = '{}'".format(Market, Date_Time, Stock))
            db.commit()
  
def update_equity(UserID):
    
    Equity = 0
    Date_Time = date_time() 
    
    mycursor.execute("SELECT cash FROM user WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Cash = x[0]
    
    mycursor.execute("SELECT (shares * price) FROM portfolio INNER JOIN stocks ON portfolio.stock = stocks.stock WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Equity = Equity + x[0]
       
    Equity_Data = [UserID, Equity, Cash, Date_Time]
    Q1 = "INSERT INTO equity (UserID, equity, cash, date_time) VALUES (%s,%s,%s,%s)"
    mycursor.execute(Q1, Equity_Data)
    db.commit()
          
def refresh():
     
    update_stocks()
    
    Users = []
    mycursor.execute("SELECT UserID FROM user")
    for x in mycursor:
        Users.append(x[0])
        
    for UserID in Users:
        update_equity(UserID)

    
def show_table(UserID):    
    
    Table_Data = []
    mycursor.execute("SELECT portfolio.stock, shares, total_cost, avg_cost_per, price FROM portfolio INNER JOIN stocks ON portfolio.stock = stocks.stock WHERE UserID = {}".format(UserID))
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
        print("\nNo stock data yet.")    
    else:
        table = tabulate(Table_Data, headers=['Stock', 'Shares', 'Total Cost', 'Average Cost', 'Equity', 'Profit', '% return'], tablefmt='orgtbl')
        print("\n",table,"\n")
    
def show_balance(UserID):
    
    Initial = 200000.00
    mycursor.execute("SELECT Balance FROM equity WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Balance = float(x[0])
        
    Profit = float(Balance - Initial)
    Return = float(((Balance / Initial)- 1) * 100)
    print("\nCurrent Balance: ${:0.2f}\nTotal Profit/Loss: ${:0.2f}\nTotal Pecent Return: {:0.4f}%\n".format(Balance, Profit, Return))

def show_graph(UserID):
    
    Graph_Data = []
    mycursor.execute("SELECT date_time, Balance FROM equity WHERE UserID = {}".format(UserID))
    for x in mycursor:
        Graph_Data.append(x)
        
    df = DataFrame (Graph_Data,columns=['Date','Balance'])
    df['Balance'] = df['Balance'].astype(float)
    df.plot(x = 'Date', y = 'Balance')

    plt.show()

def view_portfolio(UserID):
    
    refresh()
    # update_equity(UserID)
    show_table(UserID)
    show_balance(UserID)
    show_graph(UserID)
    
     
    
def rank_data():
    
    Rank_Data = []
    mycursor.execute("SET SESSION sql_mode=''")
    mycursor.execute("SELECT user_name, Balance FROM user INNER JOIN equity ON user.UserID = equity.UserID GROUP BY user_name")
    for x in mycursor:
        Rank_Data.append(x) 
        
    return Rank_Data

def rank_sort():  
    
    Initial = 200000.00
    
    Rank_Data = rank_data()
    Rank_Data.sort(key = lambda x: x[1], reverse = True)
        
    import math
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
    rank = ([ordinal(n) for n in range(1,100)])
    n = 0
    
    Rank_List = []
    for x in Rank_Data:
        user_name = x[0]
        Balance = float(x[1])
        Return = float(((Balance / Initial)-1)*100)
        Rank = rank[n]
        
        l = [user_name, "${:0.2f}".format(Balance), "{:0.4f}%".format(Return), Rank]
        Rank_List.append(l)
        n +=1
        
    return Rank_List
   
def rank_display():
    
    Data = rank_sort()
    
    print("\n")    
    table = tabulate(Data, headers=["User", "Balance", "% Return", "Rank"], tablefmt='orgtbl')
    print(table,"\n")
    


def awards_menu(UserID):
     while True:
        action = input("1. view awards \n2. suggest an award \n3. exit\n(select an option): ")
            
        if action == '1':
            print_awards()
            
            continue
        
        if action == '2':
            suggest_award(UserID)
            
            continue
    
        if action == '3':
           
            print("\n")
            break
        break
    
def print_awards():
    
    award_list = [("BULL GOD:","The Bull God is the God of returns. This trader has the most successful portfolio, the most chicken tendies, and the biggest pp (bull sized)."),
                  ("AUTISMO 9000:","Autismo 9000 is a retard; his portfolio is the worst performing on the platform (little to no tendies)."),
                  ("DADDY ELON:","This trader loves to buy tesla stock. ‘pwease daddy Ewon, can I hav sum mor gainz uwu.’"),
                  ("LONG TERM POSITION KING:","Any trader who owns Drive Shack equity"),
                  ("CAPITALIST CHAD:","The trader with the most AMZN stock."),
                  ("COMMIE TRAITOR:","Any trader who owns Alibaba - NYSE(BABA)."),
                  ("STEPHEN TOMZAC:","If a trader earns $17.3k in profit they shall receive the Stephen Tomzac award (whoever wins this award is obviously Stephen Tomzac)."),
                  ("420 WEED SMOKER:","Any trader who owns CGC, CRON, GWPH, or MJ."),
                  ("SILICON TIDDIES:","Trader with most combined stock in FB, GOOGL, or AAPL."),
                  ("AFFIRMATIVE ACTION:","The trader with the most diverse portfolio."), 
                  ("SEND IT:","A trader who owns equity in just one company.")]
    
    coming_awards = [("SHKRELI BRO:","To earn this award, you must be a true pharma bro by owning the most combined equity in pharmaceuticals.")]
    
    print("AWARDS:\n")
    for x in award_list:
        print(x[0])
        print(x[1],"\n")
        
    print("COMING AWARDS:\n")
    for x in coming_awards:
        print(x[0])
        print(x[1],"\n")

def suggest_award(UserID):

    award_name = input("Award Name: ")
    desc = input("Award Description: ")
    
    Date_Time = date_time()
    
    suggestion = [UserID, award_name, desc, Date_Time]
    
    Q = "INSERT INTO suggestions (UserID, award, descript, date_time) VALUES (%s,%s,%s,%s)"
    mycursor.execute(Q, suggestion)
    db.commit()
        
    print("\nThanks for the suggestion!\n")



def update_user_menu(UserID):
    action = input("\n1. update email\n2. update phone number\n3. reset password\n4. exit \n(select an option): ")
        
    if action == "1":
        return_statement = update_email(UserID)
        print("\n",return_statement,"\n")
        
    if action == "2":
        return_statement = update_phone(UserID)
        print("\n",return_statement,"\n")     
        
    if action == '3':
        return_statement = update_pw(UserID)
        print("\n",return_statement,"\n")
        
    if action == '4':
        return 

def update_email(UserID):
    
    while True:
        
        new_email = input("Enter email address:\n(type '%' to cancel): ")
        if new_email != '%':
        
            valid = check_email(new_email)
            if valid == 'False':
                print("\nplease enter a vaild email address.")
                continue
                
            verify_email = input("Verify email address: ")
        
            if new_email == verify_email:
                mycursor.execute("SET SQL_SAFE_UPDATES = 0")
                mycursor.execute("UPDATE user SET email = '{}' WHERE UserID = {}".format(new_email, UserID))
                mycursor.execute("SET SQL_SAFE_UPDATES = 1")
                db.commit()
                
                return_statement = "email updated successfully"
                return return_statement
    
            else:
                print("\nemails do not match.")
                action = input("1. try again\n2. exit\n")
                
                if action == "1":
                    continue
                
                if action == "2":
                    return_statement = "email address not updated"
                    return return_statement
        
        elif new_email == '%':
            return_statement = "email address not updated"
            return return_statement 

def update_phone(UserID):
    
    while True:
        
        new_value = input("Enter phone number:\n(type '%' to cancel): ")
        if new_value != '%':
            
            new_value = '{}-{}-{}'.format(new_value[0:3], new_value[3:6], new_value[6:])
            valid = check_phone(new_value)
            if valid == False:
                print("\nplease enter a vaild phone number.")
                continue
            
            verify_value = input("Verify phone number: ")
            verify_value = '{}-{}-{}'.format(verify_value[0:3], verify_value[3:6], verify_value[6:])
        
            if new_value == verify_value:
                mycursor.execute("SET SQL_SAFE_UPDATES = 0")
                mycursor.execute("UPDATE user SET phone = '{}' WHERE UserID = {}".format(new_value, UserID))
                mycursor.execute("SET SQL_SAFE_UPDATES = 1")
                db.commit()
                
                return_statement = "phone number updated successfully"
                return return_statement
    
            else:
                print("\nphone numbers do not match.")
                action = input("1. try again\n2. exit\n")
                
                if action == "1":
                    continue
                
                if action == "2":
                    return_statement = "phone number not updated"
                    return return_statement
        
        elif new_value == '%':
            return_statement = "phone number not updated"
            return return_statement 

def update_pw(UserID):
    
    while True:
        
        old_value = input("Enter current password:\n(type '%' to cancel): ")
        
        if old_value == '%':
            return_statement = "password not updated"
            return return_statement         
        
        else:
            mycursor.execute("SELECT pass_word FROM user WHERE UserID = {}".format(UserID))
            for x in mycursor:
                value_check = x[0]
            
            if old_value != value_check:
                print("\nincorrect password")
                continue
            
            else:
            
               while True:
                   
                    new_value = input("Create a password: ")
                    valid = check_pw(new_value)
                    if valid == False:
                        continue
                    verify_value = input("Verify password: ")
                
                    if new_value == verify_value:
                        mycursor.execute("SET SQL_SAFE_UPDATES = 0")
                        mycursor.execute("UPDATE user SET pass_word = '{}' WHERE UserID = {}".format(new_value, UserID))
                        mycursor.execute("SET SQL_SAFE_UPDATES = 1")
                        db.commit()
                        
                        return_statement = "password updated successfully"
                        return return_statement
            
                    else:
                        print("\npasswords do not match.")
                        action = input("1. try again\n2. exit\n")
                        
                        if action == "1":
                            continue
                        
                        if action == "2":
                            return_statement = "password not updated"
                            return return_statement   
    
    
    
def check_email(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex,email)):  
        return True
          
    else:  
        return False

def check_phone(phone):
    
    pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    return pattern.match(phone) is not None
    
def check_user_name(user_name):
    
    mycursor.execute("SELECT user_name FROM user")
        
    while True:
        for x in mycursor:
            if x[0] == user_name:
                return False
        
        return True
    
def check_pw(password):
    
    regex = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    
    if (re.findall(regex,password)):
        return True
    
    else:
        print("Password must contain at least 8 characters\nMust be restricted to, though does not specifically require any of:\nuppercase letters: A-Z\nlowercase letters: a-z\nnumbers: 0-9\nany of the special characters: @#$%^&+=")
        return False
        

def check_DOB(DOB):
    
   try:
       datetime.strptime(DOB,"%m/%d/%Y")
   except ValueError as err:
       return False
           
   return True
      
 

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
    
    # years = mdates.YearLocator()   # every year
    # months = mdates.MonthLocator()  # every month
    # week = mdates.WeekdayLocator()
    # hour = mdates.HourLocator()
    # minute = mdates.MinuteLocator()
    
    # years_fmt = mdates.DateFormatter('%Y')
    
    # Range = day()
    # Min = Range[0]
    # Max = Range[1]
    
    
    # data = []
    # mycursor.execute("SELECT date_time, Balance FROM Equity WHERE UserID = {}".format(UserID))
    # for x in mycursor:
    #     data.append(x)
    
    # df = DataFrame (data,columns=['Date','Balance'])
    # df['Balance'] = df['Balance'].astype(float)
    # df.plot(x = 'Date', y = 'Balance')
    # # fig, df = plt.subplots()
    # # fig.autofmt_xdate()
    # df.set_xlim([datetime.date(Min), datetime.date(Max)])
    # # df.set_ylim([0, 5])
    # plt.show()
    
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
    
    plt.show()

  


def test():
    
    while True:
         password = input("Create a password: ")
         valid = check_pw(password)
         if valid == False:
             continue
         else:
             break



# rank_display()

