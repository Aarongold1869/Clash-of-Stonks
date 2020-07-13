# -*- coding: utf-8 -*-
"""
Created on Fri Jul 3 17:11:09 2020

@author: Aaron Goldstein
"""

## pulls stonk data from Alpha Vantage API
import requests
import alpha_vantage
## Alpha_Vantage API Key
API_KEY = 'GFUV3575DL68NYGL'
## command imports data from AV API and uses Python Pandas to format data
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(API_KEY, output_format = 'pandas')

## allows operation on JSON objects and files
import json

## allows for creation of graphs and charts based on stonk data
import matplotlib.pyplot as plt

## tabulate module formats specified data in print statement table
from tabulate import tabulate 
    
## module pulls date time data
from datetime import datetime

## pandas dataframe module for formatting data
from pandas import DataFrame

## conects to MySQL Database
import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "stonkdb"
    )
## iterates through MySQL data stored in tables
mycursor = db.cursor()

## describe mysql table(s) in stonkdb
def describetable():
    mycursor.execute("DESCRIBE Portfolio")
    for x in mycursor: 
        print(x)

## print mysql table(s) in stonkdb
def printtables():
    mycursor.execute("SELECT * FROM portfolio")
    for x in mycursor:
        print(x)
        
    # mycursor.execute("SELECT * FROM User")
    # for x in mycursor:
    #     print(x)
    
    # mycursor.execute("SELECT * FROM User_Balance")
    # for x in mycursor:
    #     print(x)

## truncate portfolio table
def trunkport():
    mycursor.execute("TRUNCATE TABLE stonkdb.portfolio")
    db.close()

## truncate User_Balance table
def trunkbal():
    mycursor.execute("TRUNCATE TABLE stonkdb.User_Balance")
    db.close()

## truncate User table
def trunkuser():
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("TRUNCATE table stonkdb.User") 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close

## delete portfolio table
def dropport():
    mycursor.execute("DROP TABLE stonkdb.portfolio")
    db.close()

## delete user table
def dropuser():
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("DROP TABLE stonkdb.User") 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close

## retrieve user input for creating user account
def userinfo():    
    ## Set initial Cash Balance
    Cash = 200000

    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    age = input("What is your age?: ")
    email = input("What is your email?: ")
    phone = input("What is your phone?: ")
    user_name = input("Create a user name: ")
    password = input("Create a password: ")
    
    # store user account info in list to be uploaded to mysql database
    User_info = [(first_name,
                  last_name,
                  age,
                  email,
                  phone,
                  user_name,
                  password,
                  Cash)]
    
    # welcome message
    Introduction = "\nHey {}! You have ${} to invest. Let's get started!".format(user_name, Cash)
    print(Introduction)
    
    # return account info (to be used in userload function)
    return User_info

## create user record in User table
def userload():
    # User data collected from userinfo function
    User_info = userinfo()
    
    # store Cash value in seperate variable
    Cash = User_info[-1][-1]
    # store User_name in seperate variable - used to retrieve UserID
    User_name = User_info[-1][-3]
    
    # create list containing all variables except Cash (Cash stored in portfolio table)
    temp = []
    for x in User_info[0][:-1]:
          temp.append(x)
    
    ## format list data for db uplaod 
    user_record =[(temp)]
    
    # Query 1 Create user record in User table. Query 2 create record in Portfolio table (intial Cash Value) with FK UserID
    user_load = "INSERT INTO User (first_name, last_name, age, email, phone, user_name, password) VALUES(%s,%s,%s,%s,%s,%s,%s)"  
    Port_load = "INSERT INTO Portfolio (UserID, cash) VALUES (%s, %s)"
    
    # execute Query1 - create user record using user info list
    for x, user in enumerate(user_record):
        mycursor.execute(user_load, user)  
    db.commit()
   
    # retrieve UserID value (auto increment Int) from User record 
    mycursor.execute("SELECT UserID FROM User WHERE user_name = '{}'".format(User_name))
    for x in mycursor:
        UserID = x[0]   
    
    # store UserID and Cash variables in list 
    new_record = [UserID, Cash]
        
    # create portfolio record in database with UserID FK and initial Cash variable from new_record list
    mycursor.execute(Port_load, new_record)
    db.commit()    
    
    # Return UserID to main
    return UserID
    
## allow existing user to login (return UserID to main)
def login():
    
    Valid = True
    while Valid == True:
        User_name = input("Username: ")
        password = input("Password: ")
        
        mycursor.execute("SELECT UserID FROM User WHERE user_name = '{}' AND password = '{}'".format(User_name,password))
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
            print("\nHey, {}!".format(User_name))
            return UserID
            
## retreive purchase info from User input 
def purchaseinfo(UserID):                            
    mycursor.execute("SELECT cash FROM Portfolio WHERE userID = {}".format(UserID))
    for x in mycursor:
        Cash = float(x[0])
    
    invest = True
    while invest == True:  
        ## retreive user input, retreive stonk data, display stonk data
        Stonk = input("Insert a stock ticker or type '%' to cancel: ")
        
        if Stonk == '%':
            invest = False
            Port_Data = "false"
            return Port_Data
        
        else:
            values_1, columns = ts.get_intraday(symbol = Stonk)
            values_1['4. close'].plot()
            plt.show()
            print(values_1)
        
        ## retrieves last market value of stock from array and converts to integer
            Market = float(values_1['4. close'][0])
            
            ## displays stock price of user requested sotck and asks for user input
            Mkt_String = "{} is trading at ${:0.2f}. Would you like to buy equity in {}?".format(Stonk, Market, Stonk)
            print(Mkt_String)
            Action = input('1. Yes\n2. No\n')
            
            Buy = True
            while Buy == True:
                ## user input - if user does not want to purchase stock, break while loop    
               
                ##if user would like to purchase stock, display remaining money, get input on how many shares to purchase
                if Action =='1':   
                    Cash_string = "You have ${:0.2f}".format(Cash)
                    print(Cash_string)
            
                    Shares = int(input("How many shares would you like to buy? Enter # of shares:\npress '0' to cancel\n"))
                    
                    if Shares != 0:
                        invest = float(Shares * Market)
                   
                    ##if user can afford number of shares requeste
                        
                        if (Cash - invest) > 0:
                            ##subtract shares purchased from cash
                            Cash = float(Cash - invest)
                              
                            ##display user equit
                            Equity_String = "\nYou own {} share(s) of {} Congratulations!".format(Shares,Stonk)
                
                            ##display remaining investable cash
                            Cash_String = "you have ${:0.2f} left to invest\n".format(Cash)
                            print(Equity_String, Cash_String)
                            
                            from datetime import datetime
                            now = datetime.now()
                            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                            
                            Port_Data = [(UserID,
                                          dt_string,
                                          Stonk,
                                          Shares, 
                                          Market, 
                                          Market, 
                                          invest, 
                                          Cash)]
                            
                            return Port_Data
                          
                        else:
                            ##alert user of insufficient funds
                            print('\nYou dont have enough money.')
                            ## start loop over 
                            continue
                        continue
                        
                    else:
                        break
                    
                    
                elif Action == '2':
                   break
                break
            continue
        
## create purchase record in Portfolio database 
def portload(UserID):
    Port_Data = purchaseinfo(UserID)
    
    if Port_Data == 'false':
        print("\nNo purchase was made\n")
        
    else:
        Port_load = "INSERT INTO Portfolio (UserID, date_time, stonks, shares, cost, mkt_price, total_val, cash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(Port_Data):
            mycursor.execute(Port_load, data)
        db.commit()
    
## View user portfolio data 
def portview(UserID):
    #pull the last cash value stored in the Portfolio table
    mycursor.execute("SELECT cash FROM Portfolio WHERE userID = {}".format(UserID))
    for x in mycursor:
        #assign most recent cash value to variable 'Cash'
        Cash = float(x[-1])
    
    #create a list for storing the names of stonks owned in a portfolio
    stonklist = []
    #select all stonks from user portfolio 
    mycursor.execute("SELECT stonks FROM Portfolio WHERE userID = {}".format(UserID))
    for x in mycursor:
        #write stonks in portfolio table into a list 
        stonklist.append(x[-1])
    #sort list into dicitionary to remove duplicate values
    stonklist = list(dict.fromkeys(stonklist))
    #(excluding the first value which is null due to intial table creation)
    del stonklist[0]    
    
    #create list for storing values to be displayed in tablulate table
    tablist = []
    #create list for storing Equity values in a given row for a given stonk
    equity_list = []
    #for each stock in the stonklist 
    for x in stonklist:
        Stonk = x
        #retrieve market value from AV API for stonk in stonklist
        value, columns = ts.get_intraday(symbol = Stonk)
        value['4. close']
        #assign most recent stock value to variable 'Market' to be used in calculations 
        Market = float(value['4. close'][0])
        
        #create list for storing number of shares per stonk
        sharelist = []
        #select all shares assosciated with a given stonk 
        mycursor.execute("SELECT shares FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, Stonk))
        for x in mycursor:
            #append shares in table to share list 
            sharelist.append(x[-1])
        
        #total all shares associated with a given stonk from each purchase order / sell order portfolio row
        total_shares = float(sum(sharelist))
        #Total Equity (current) = number of shares times current market value 
        Equity = float(total_shares * Market)
        
        #create list for storing investment costs by stock by purchase order
        cost_list = []
        #pull all investment costs by stock by purchase order from portfolio table
        mycursor.execute("SELECT total_val FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, Stonk))
        for x in mycursor:
            #append purchase costs to list 
            cost_list.append(x[-1])
        
        #sum all purchase costs to get total investment for a given stock - assign to variable "Cost"
        Cost = float(sum(cost_list))
        #avg cost for a given stonk is Total investment Cost / Total shares 
        avg_cost = float(Cost / total_shares)
        #Profit by stock = total Current equity - Total intitial investment cost
        profit = float(Equity - Cost)
        #percent return for a given stock = Equity / cost -1 *100
        percent = ((Equity / Cost)-1) * 100
        
        #Store variable values in a string to be formatted in table by tabulate module 
        l = [Stonk, total_shares, "${:0.2f}".format(avg_cost), "${:0.2f}".format(Cost), "${:0.2f}".format(Equity), "${:0.2f}".format(profit), "{:0.4f}%".format(percent)]
        tablist.append(l) 
        
        #append Equity value by stonk to list to calculate total current portfolio value 
        equity_list.append(Equity)
        # Update mareket price column in Portfolio for all rows for a given stonk 
        # mycursor.execute("UPDATE Portfolio SET mkt_price = {} WHERE userID = {} AND stonks = '{}'".format(Market, UserID, Stonk))

    #create / display table using variables collected in for loop - display equity, return, etc. by stonk
    table = tabulate(tablist, headers=['Stock', 'Shares', 'Average Cost', "Total Cost", 'Equity', 'Profit', '% return'], tablefmt='orgtbl')
    print(table)
    
    #Total equity variable = sum of equity by stock (from list created in for loop)
    Total_Equity = float(sum(equity_list))
    #Total portfolio balance = Total Equity + Cash balance
    Balance = float(Cash + Total_Equity)
    
    mycursor.execute("SELECT cash FROM Portfolio WHERE UserID ={} LIMIT 1".format(UserID))
    for x in mycursor:
        Initial = float(x[0])
   
    Profit = Balance - Initial
    Return = ((Balance / Initial)-1)*100
    
    #create datetime string for storing longitudinal data
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    
    #create list of values to import into User_Balance table - User balance table created to display portfolio growth/loss
    b_list = [(UserID, dt_string, Total_Equity, Cash, Balance, Return)]
    #assign MySQL command to "b_load" Variable - updload balance variables to Balance Table
    b_load = "INSERT INTO User_Balance (UserID, date_time, Equity, Cash, Balance, percent_return) VALUES (%s, %s, %s, %s, %s, %s)"   
    #for values in list
    for x, data in enumerate(b_list):
        #upload values to table 
        mycursor.execute(b_load, data)
    #save data to database
    db.commit()
     
    #Create lsit for storing specific portfolio values to display balance data in matplot graph
    graph = []          
    #select Date and Balance from User Balance Table 
    mycursor.execute("SELECT date_time, Balance FROM User_Balance WHERE userID = {}".format(UserID))
    #write dat into list 
    for x in mycursor:
        graph.append(x)
    
    #write balance data from list into pandas dataframe - plot data frame data in matplot 
    df = DataFrame (graph,columns=['Date','Balance'])
    df['Balance'] = df['Balance'].astype(float)
    df.plot(x = 'Date', y = 'Balance')
    plt.show()
    print("\nCurrent Balance: ${:0.2f}\nTotal Profit/Loss: ${:0.2f}\nTotal Pecent Return: {:0.4f}%\n".format(Balance, Profit, Return))

## retreive sell info from User input
def sellinfo(UserID):   
    Sell = True
    while Sell == True: 
        
        stonk_sell = input("Which stock would you like to sell?\n(Insert stock ticker. Press '%' to cancel.):")
        
        if stonk_sell == '%':
            Sell = False
            Sell_Data = "false"
            return Sell_Data
        
        else:
            mycursor.execute("SELECT cash FROM Portfolio WHERE userID = {}".format(UserID))
            for x in mycursor:
                #assign most recent cash value to variable 'Cash'
                Cash = float(x[-1])
            
            value, columns = ts.get_intraday(symbol = stonk_sell)
            value['4. close']
            Market_sell = float(value['4. close'][0])
            
            shares_sell = int(input("{} is trading at ${}. How many shares would you like to sell?\n(Type '0' to cancel.)".format(stonk_sell, Market_sell)))
            
            Sell_Clause = True
            while Sell_Clause == True:
    
                if shares_sell != 0: 
                    debit = float(shares_sell * Market_sell)
                    Cash = Cash + debit
                    
                    print("\nCongrats! You sold {} shares of {} for a debit to your account of ${}.\n".format(shares_sell, stonk_sell, debit))
                
                    shares_sell = (shares_sell * (-1))
                    debit = (debit * (-1))
                    
                    mycursor.execute("SELECT total_val FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, stonk_sell))
                    for x in mycursor:
                        #append purchase costs to list 
                        cost_list.append(x[-1])
                    
                    #sum all purchase costs to get total investment for a given stock - assign to variable "Cost"
                    Cost = float(sum(cost_list))
                    #avg cost for a given stonk is Total investment Cost / Total shares 
                    avg_cost = float(Cost / total_shares)
                    
                    now = datetime.now()
                    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                    
                    Sell_Data = [(UserID,
                                  dt_string,
                                  stonk_sell,
                                  shares_sell, 
                                  avg_cost, 
                                  Market_sell, 
                                  debit, 
                                  Cash)]
                        
                    return Sell_Data
                
                else:
                    Sell = False
                    Sell_Data = "false"
                    return Sell_Data
               
## create sell record in Portfolio database
def sell_load(UserID):
    Sell_Data = sellinfo(UserID)
    
    if Sell_Data == 'false':
        print("\nNo sale was made\n")
        
    else:
        Sell_load = "INSERT INTO Portfolio (UserID, date_time, stonks, shares, cost, mkt_price, total_val, cash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(Sell_Data):
            mycursor.execute(Sell_load, data)
        db.commit()

## view all users ranked on portfolio performance 
def rank():
    
    id_list =[]
    mycursor.execute("SELECT UserID FROM User")
    for x in mycursor:
        id_list.append(x[-1])
    
    rank_list = []
    for ID in id_list:
        mycursor.execute("SELECT User.user_name, User_Balance.Balance, User_Balance.percent_return FROM User, User_Balance WHERE User.UserID ={} AND User_Balance.UserID = {} ORDER BY balID DESC LIMIT 1".format(ID,ID))
        for x in mycursor:
            rank_list.append(x)
            
    # print(rank_list)
    table = tabulate(rank_list, headers=["User", "Balance", "Total Return"], tablefmt='orgtbl')
    print(table)
  

# userload()
# portload()
# printtables()
# test()
# login()
# trunkport()
# trunkuser()
# trunkbal()
# describetable()

