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

#sleep pauses program to prevent exceed API maximum call frequency
from time import sleep

## pandas dataframe module for formatting data
from pandas import DataFrame

import re

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
    mycursor.execute("DESCRIBE User")
    for x in mycursor: 
        print(x)

## print mysql table(s) in stonkdb
def printtables():
    # mycursor.execute("SELECT * FROM portfolio")
    # for x in mycursor:
    #     print(x,"\n")
        
    mycursor.execute("SELECT * FROM User")
    for x in mycursor:
        print(x,"\n")
    
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
    
    password = input("Create a password: ")
    
    # store user account info in list to be uploaded to mysql database
    User_info = [(first_name,
                  last_name,
                  DOB,
                  email,
                  phone,
                  user_name,
                  password,
                  Cash)]
    
    # welcome message
    Introduction = "\nHey {}! You have ${} to invest. Let's get started!".format(user_name, Cash)
    print(Introduction)
    
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
    
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    
    temp.append(dt_string)
    ## format list data for db uplaod 
    user_record =[(temp)]
    
    # Query 1 Create user record in User table. Query 2 create record in Portfolio table (intial Cash Value) with FK UserID
    user_load = "INSERT INTO User (first_name, last_name, DOB, email, phone, user_name, password, date_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"  
    
    # execute Query1 - create user record using user info list
    for x, user in enumerate(user_record):
        mycursor.execute(user_load, user)  
    db.commit()
   
    # retrieve UserID value (auto increment Int) from User record 
    mycursor.execute("SELECT UserID FROM User WHERE user_name = '{}'".format(User_name))
    for x in mycursor:
        UserID = x[0]   
    
    # store UserID and Cash variables in list 
    Equity = 0
    Balance = Equity + Cash
    Return = ((Balance / Cash)-1)*100
    
    
    new_record = [UserID, dt_string, Equity, Cash, Balance, Return]
    Cash_load = "INSERT INTO User_Balance (UserID, date_time, Equity, Cash, Balance, percent_return) VALUES (%s,%s,%s,%s,%s,%s)"
    
    # create portfolio record in database with UserID FK and initial Cash variable from new_record list
    mycursor.execute(Cash_load, new_record)
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
            
    
def API_call(Stonk):

    while True:
        
        try:
            values_1, columns = ts.get_intraday(symbol = Stonk)
            return values_1
        
        except ValueError:
            continue
    


## retreive purchase info from User input 
def purchaseinfo(UserID):                            
    mycursor.execute("SELECT cash FROM User_Balance WHERE userID = {}".format(UserID))
    for x in mycursor:
        Cash = float(x[0])
    
    invest = True
    while invest == True:  
        ## retreive user input, retreive stonk data, display stonk data
        Stonk = input("Insert a stock ticker or type '%' to cancel: ")
        
        if Stonk == '%':
            invest = False
            Purchase_Data = "false"
            return Purchase_Data
        
        else:
            values_1 = API_call(Stonk)
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
                            New_Cash = float(Cash - invest)
                              
                            
                            Equity_String = "\nYou purchased {} share(s) of {} Congratulations!".format(Shares,Stonk)
                            Cash_String = "you have ${:0.2f} left to invest\n".format(New_Cash)
                            print(Equity_String, Cash_String)
                            
                            
                            now = datetime.now()
                            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                            
                            Purchase_Data = [(UserID,
                                          dt_string,
                                          Stonk,
                                          Shares, 
                                          Market, 
                                          Market, 
                                          invest
                                          )]
                            
                            Balance_Data = [(UserID, dt_string, invest, New_Cash)]
                            
                            
                            return Purchase_Data, Balance_Data
                          
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
def purchaseload(UserID):
    Data = purchaseinfo(UserID)
    
    if Data == 'false':
        print("\nNo purchase was made\n")
    
    else:        
        Purchase_Data = Data[0]
        Balance_Data = Data[1][0]
        
        
        Port_info = port_info(UserID)
            
        Old_Equity = Port_info[0][0][2]
        datetime = Port_info[0][0][1]
        Return = Port_info[0][0][5]
        
        New_Equity = Balance_Data[2] 
        New_Cash = Balance_Data[3]
        
        Total_Equity = Old_Equity + New_Equity
        Cash = New_Cash
        Balance = Total_Equity + Cash
        
        new_record = [(UserID, datetime, Total_Equity, Cash, Balance, Return)]
                
        b_load = "INSERT INTO User_Balance (UserID, date_time, Equity, Cash, Balance, percent_return) VALUES (%s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(new_record):
            mycursor.execute(b_load, data)
        db.commit()
        
        
        Port_load = "INSERT INTO Portfolio (UserID, date_time, stonks, shares, cost, mkt_price, total_val) VALUES (%s, %s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(Purchase_Data):
            mycursor.execute(Port_load, data)
        db.commit

        
        
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
            mycursor.execute("SELECT cash FROM User_Balance WHERE userID = {}".format(UserID))
            for x in mycursor:
                #assign most recent cash value to variable 'Cash'
                Cash = float(x[-1])
            
            value = API_call(stonk_sell)
            value['4. close']
            Market_sell = float(value['4. close'][0])
            
            sharelist = []
            #select all shares assosciated with a given stonk 
            mycursor.execute("SELECT shares FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, stonk_sell))
            for x in mycursor:
                #append shares in table to share list 
                sharelist.append(x[-1])
            
            #total all shares associated with a given stonk from each purchase order / sell order portfolio row
            total_shares = float(sum(sharelist))
            #Total Equity (current) = number of shares times current market value 
            
            cost_list = []
            mycursor.execute("SELECT total_val FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, stonk_sell))
            for x in mycursor:
                #append purchase costs to list 
                cost_list.append(x[-1])
            
            #sum all purchase costs to get total investment for a given stock - assign to variable "Cost"
            Cost = float(sum(cost_list))
            #avg cost for a given stonk is Total investment Cost / Total shares 
            avg_cost = float(Cost / total_shares)
            
            Sell_Clause = True
            while Sell_Clause == True:
               
                shares_sell = int(input("{} is trading at ${}. How many shares would you like to sell?\n(Type '0' to cancel.)".format(stonk_sell, Market_sell)))
                
                if shares_sell != 0: 
                    debit = float(shares_sell * Market_sell)
                    Cash = Cash + debit
                    inv = total_shares - shares_sell
                    
                    if inv >= 0:
                        print("\nCongrats! You sold {} shares of {} for a debit to your account of ${:0.2f}.\n".format(shares_sell, stonk_sell, debit))
                    
                        shares_sell = (shares_sell * (-1))
                        debit = (debit * (-1))
                        
                        now = datetime.now()
                        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                        
                        Sell_Data = [(UserID,
                                      dt_string,
                                      stonk_sell,
                                      shares_sell, 
                                      avg_cost, 
                                      Market_sell, 
                                      debit
                                      )]
                        
                        Balance_Data = [(UserID, dt_string, debit, Cash)]
                        
                        return Sell_Data, Balance_Data
                
                    else:
                        print("\nYou cannot sell that many shares, you only own {} shares of {}.".format(total_shares, stonk_sell))
                        continue
                    break 
                
                else:
                    Sell = False
                    Sell_Data = "false"
                    return Sell_Data
               
## create sell record in Portfolio database
def sell_load(UserID):
    Data = sellinfo(UserID)
    
    if Data == 'false':
        print("\nNo sale was made\n")
        
    else:
        Purchase_Data = Data[0]
        Balance_Data = Data[1][0]
       
        
        Port_info = port_info(UserID)
            
        Old_Equity = Port_info[0][0][2]
        datetime = Port_info[0][0][1]
        Return = Port_info[0][0][5]
        
        New_Equity = Balance_Data[2] 
        New_Cash = Balance_Data[3]
        
        Total_Equity = Old_Equity + New_Equity
        Cash = New_Cash
        Balance = Total_Equity + Cash
        
        new_record = [(UserID, datetime, Total_Equity, Cash, Balance, Return)]
                
        b_load = "INSERT INTO User_Balance (UserID, date_time, Equity, Cash, Balance, percent_return) VALUES (%s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(new_record):
            mycursor.execute(b_load, data)
        db.commit()
        
        
        Port_load = "INSERT INTO Portfolio (UserID, date_time, stonks, shares, cost, mkt_price, total_val) VALUES (%s, %s, %s, %s, %s, %s, %s)"   
        for x, data in enumerate(Purchase_Data):
            mycursor.execute(Port_load, data)
        db.commit
    
        #######################################################################
        # if all shares of stock sold -- delete stock from Portfolio Table : 
        # THIS FUNCTIONALITY ONLY NECESSARY WHEN API CALL FREQ LIMIT IN EFFECT 
        # PREVENETS UNNECESSARY DELAYS IN PORTFOLIO VIEW TIME.
        ######################################################################
        
        # Stonk = Purchase_Data[-1][2]
        # sharelist = []
        # #select all shares assosciated with a given stonk 
        # mycursor.execute("SELECT shares FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, Stonk))
        # for x in mycursor:
        #     #append shares in table to share list 
        #     sharelist.append(x[-1])
        
        # #total all shares associated with a given stonk from each purchase order / sell order portfolio row
        # total_shares = float(sum(sharelist))
        
        # if total_shares == 0:
        #     mycursor.execute("DELETE FROM Portfolio WHERE userID = {} AND stonks = '{}'".format(UserID, Stonk))
        # db.commit 
                
        
        
## View user portfolio data 
def port_info(UserID):
    
    #pull the last cash value stored in the Balance table
    mycursor.execute("SELECT cash FROM User_Balance WHERE userID = {}".format(UserID))
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

        
    #create list for storing values to be displayed in tablulate table
    tablist = []
    #create list for storing Equity values in a given row for a given stonk
    equity_list = []
    #for each stock in the stonklist 
    
    for x in stonklist:
        Stonk = x
        #retrieve market value from AV API for stonk in stonklist
        value = API_call(Stonk)
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
        if total_shares == 0:
            continue
        
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
        avg_cost = (Cost / total_shares)
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
    
    
    Total_Equity = float(sum(equity_list))
    Balance = float(Cash + Total_Equity)
    
    mycursor.execute("SELECT cash FROM User_Balance WHERE UserID ={} LIMIT 1".format(UserID))
    for x in mycursor:
        Initial = float(x[0])
   
    Profit = Balance - Initial
    Return = ((Balance / Initial)-1)*100
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    
    load_list = [(UserID, dt_string, Total_Equity, Cash, Balance, Return)]
    b_list = [Balance, Profit, Return]
    
    
    graph = []          
    mycursor.execute("SELECT date_time, Balance FROM User_Balance WHERE userID = {}".format(UserID))
    for x in mycursor:
        graph.append(x)
    
    
    return load_list, b_list, tablist, graph
    
## load portfolio / balance data into database
def port_load(UserID): 
    
    data = port_info(UserID)
    
    load_list = data[0]
    b_list = data[1]
    tablist = data[2]
    graph = data[3]
             
    mycursor.execute("set innodb_lock_wait_timeout=1000")
    b_load = "INSERT INTO User_Balance (UserID, date_time, Equity, Cash, Balance, percent_return) VALUES (%s, %s, %s, %s, %s, %s)"   
    for x, data in enumerate(load_list):
        mycursor.execute(b_load, data)
    db.commit()
    
    
    return load_list, b_list, tablist, graph

## display portfolio / balance data
def port_display(UserID):
    print("\nloading...\n")
    
    data = port_load(UserID)
    b_list = data[1]
    tablist = data[2]
    graph = data[3]
    
    
    if not tablist:
        print("No stock data yet.")    
    else:
        table = tabulate(tablist, headers=['Stock', 'Shares', 'Average Cost', "Total Cost", 'Equity', 'Profit', '% return'], tablefmt='orgtbl')
        print(table)

    # graph = graph[0::1]
    df = DataFrame (graph,columns=['Date','Balance'])
    df['Balance'] = df['Balance'].astype(float)
    df.plot(x = 'Date', y = 'Balance')
    plt.show()
    
    
    Balance = float(b_list[0])
    Profit = float(b_list[1])
    Return = float(b_list[2])
    print("\nCurrent Balance: ${:0.2f}\nTotal Profit/Loss: ${:0.2f}\nTotal Pecent Return: {:0.4f}%\n".format(Balance, Profit, Return))
    
    

def rank_info():
    
    print("\nLoading...\n")
    
    id_list =[]
    mycursor.execute("SELECT UserID FROM User")
    for x in mycursor:
        id_list.append(x[-1])
    
    ##########################################################################
    ## REFRESH BALANCE DATA FOR EVERY USER  IN SYSTEM....  ###################
    ## MORE ACCURATE REANKING, MAKES PROGRAM RUN SLOW AF...###################
        
    for ID in id_list:
        port_load(ID)
        
    #########################################################################
    
    Balance_list = []
    for ID in id_list:
        mycursor.execute("SELECT User.user_name, User_Balance.Balance, User_Balance.percent_return FROM User, User_Balance WHERE User.UserID ={} AND User_Balance.UserID = {} ORDER BY balID DESC LIMIT 1".format(ID,ID))
        for x in mycursor:
            l = [ID, x]
            Balance_list.append(l)
     
    # print(Balance_list)
    return Balance_list

def rank_sort():  
    
    tup = rank_info()
    tup.sort(key = lambda x: x[1][2], reverse = True)
        
    import math
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
    rank = ([ordinal(n) for n in range(1,100)])
    n = 0
    
    rank_list = []
    load_list = []
    for x in tup:
        UserID = x[0]
        user_name = x[1][0]
        Balance = x[1][1]
        Return = x[1][2]
        Rank = rank[n]
        
        l = [user_name, Balance, Return, Rank]
        m = [UserID, Rank]
        rank_list.append(l)
        load_list.append(m)
        n +=1
        
    return rank_list, load_list 

def rank_load():
        
    Data = rank_sort()
    rank_list = Data[0]
    load_list = Data[1]
    
    mycursor.execute("SET SQL_SAFE_UPDATES = 0")
    mycursor.execute("set innodb_lock_wait_timeout=1000")
    for x in load_list:
        UserID = x[0]
        Rank = x[1]
        mycursor.execute("UPDATE User SET Ranking = '{}' WHERE UserID = {}".format(Rank, UserID))
    db.commit 
    mycursor.execute("SET SQL_SAFE_UPDATES = 1")

    
    return rank_list
    
def rank_display():
    
    Data = rank_load()
    
    rank_list = []
    for x in Data:      
        user_name = x[0]
        Balance = float(x[1])
        Return = float(x[2])
        Rank = x[3]
        l = [user_name, "${:0.2f}".format(Balance), "{:0.4f}%".format(Return), Rank]
        rank_list.append(l)
    
    
    print("\n")    
    table = tabulate(rank_list, headers=["User", "Balance", "% Return", "Rank"], tablefmt='orgtbl')
    print(table,"\n")
    


def update_user(UserID):
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
                mycursor.execute("UPDATE USER SET email = '{}' WHERE UserID = {}".format(new_email, UserID))
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
                mycursor.execute("UPDATE USER SET phone = '{}' WHERE UserID = {}".format(new_value, UserID))
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
            mycursor.execute("SELECT password FROM USER WHERE UserID = {}".format(UserID))
            for x in mycursor:
                value_check = x[0]
            
            if old_value != value_check:
                print("\nincorrect password")
                continue
            
            else:
            
               while True:
        
                    new_value = input("Enter new password: ")
                    verify_value = input("Verify password: ")
                
                    if new_value == verify_value:
                        mycursor.execute("SET SQL_SAFE_UPDATES = 0")
                        mycursor.execute("UPDATE USER SET password = '{}' WHERE UserID = {}".format(new_value, UserID))
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
        return "True" 
          
    else:  
        return "False" 

def check_phone(phone):
    
    pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    return pattern.match(phone) is not None
    
def check_user_name(user_name):
    
    mycursor.execute("SELECT user_name FROM User")
        
    while True:
        for x in mycursor:
            if x[0] == user_name:
                return False
        
        return True

def check_DOB(DOB):
    
   try:
       datetime.strptime(DOB,"%m/%d/%Y")
   except ValueError as err:
       return False
           
   return True
      
 
def test():
    DOB = ("07/27/1995")
    DOB = datetime.strptime(DOB, "%m/%d/%Y")
    print(DOB)
    
    
    
# update_phone()
# test()

# userload()
# portload()
# printtables()
# test()
# login()
# trunkport()
# trunkuser()
# trunkbal()
# describetable()

