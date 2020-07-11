# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 17:11:09 2020

@author: Aaron Goldstein
"""

##pulls stonk data from Alpha Vantage API
import requests
import alpha_vantage
##Alpha_Vantage API Key
API_KEY = 'GFUV3575DL68NYGL'
##command pulls data from AV API and uses Python Pandas to format data
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(API_KEY, output_format = 'pandas')

##allows operation on JSON objects and files
import json

##allows for creation of graphs and charts based on stonk data
import matplotlib.pyplot as plt

from tabulate import tabulate 
    
from datetime import datetime

from pandas import DataFrame

##conects to MySQL Database
import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "stonkdb"
    )
##iterates through MySQL data stored in tables
mycursor = db.cursor()


def describetable():
    mycursor.execute("DESCRIBE User_Balance")
    for x in mycursor: 
        print(x)


def printtables():
    # mycursor.execute("SELECT * FROM portfolio")
    # for x in mycursor:
    #     print(x)
        
    # mycursor.execute("SELECT * FROM User")
    # for x in mycursor:
    #     print(x)
        
    mycursor.execute("SELECT * FROM User_Balance")
    for x in mycursor:
        print(x)


def trunkport():
    mycursor.execute("TRUNCATE TABLE stonkdb.portfolio")
    db.close()


def trunkbal():
    mycursor.execute("TRUNCATE TABLE stonkdb.User_Balance")
    db.close()


def trunkuser():
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("TRUNCATE table stonkdb.User") 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close


def dropport():
    mycursor.execute("DROP TABLE stonkdb.portfolio")
    db.close()


def dropuser():
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("DROP TABLE stonkdb.User") 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close


def userinfo():    
    ##initial Paper trading amount
    Cash = 200000

    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    age = input("What is your age?: ")
    email = input("What is your email?: ")
    phone = input("What is your phone?: ")
    user_name = input("Create a user name: ")
    password = input("Create a password: ")
    
    User_info = [(first_name,
                  last_name,
                  age,
                  email,
                  phone,
                  user_name,
                  password,
                  Cash)]

    Introduction = "Hey {}! You have ${} to invest. Let's get started!".format(user_name, Cash)
    print(Introduction)
    
    return User_info


def userload():
    User_info = userinfo()
    
    Cash = [(User_info[-1][-1],)]
    User_name = User_info[-1][-3]

    info = []
    for x in User_info[0][:-1]:
          info.append(x)
    
    User_info = [tuple(info)]
    
    user_load = "INSERT INTO User (first_name, last_name, age, email, phone, user_name, password) VALUES(%s,%s,%s,%s,%s,%s,%s)"  
    Port_load = "INSERT INTO Portfolio (UserID, cash) VALUES (%s, %s)"
    
    for x, user in enumerate(User_info):
        mycursor.execute(user_load, user)  
        last_id = mycursor.lastrowid
        mycursor.execute(Port_load,(last_id,) + Cash[x])
    db.commit()    
    
    mycursor.execute("SELECT UserID FROM User WHERE user_name = '{}'".format(User_name))
    for x in mycursor:
        UserID = x[0]
        
    return UserID
    

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
            

def purchaseinfo(UserID):                            
    mycursor.execute("SELECT cash FROM Portfolio WHERE userID = {}".format(UserID))
    for x in mycursor:
        Cash = x[0]
    
    while Cash > 0:  
        ## retreive user input, retreive stonk data, display stonk data
        Stonk = input("Insert a stonk ticker or type '%' to exit: ")
        Stonk.capitalize()
        if Stonk != '%':
            values_1, columns = ts.get_intraday(symbol = Stonk)
            values_1['4. close'].plot()
            plt.show()
            print(values_1)
            
        ##User doesnt want to invest 
        else:
            print('goodbye.')
            break
        
        ## retrieves last market value of stock from array and converts to integer
        Market = float(values_1['4. close'][0])
        
        ##while loop for viewing / purchasing a given stock
        Buy = 'Y'
        while Buy == 'Y':
            
            ##displays stock price of user requested sotck and asks for user input
            Mkt_String = "{} is trading at ${}. Would you like to buy equity in {}?".format(Stonk, Market, Stonk)
            print(Mkt_String)
            
            ##user input - if user does not want to purchase stock, break while loop
            Buy = input('Y / N: ')
            Buy.capitalize()
            if Buy == 'N':
                break
            
            ##if user would like to purchase stock, display remaining money, get input on how many shares to purchase
            else:   
                Cash_string = "You have ${}".format(Cash)
                print(Cash_string)
        
                Shares = int(input("How many shares would you like to buy? Enter # of shares: "))
                invest = int(Shares * Market)
                
                
                ##if user can afford number of shares requeste
                if Cash - invest > 0:
                    ##subtract shares purchased from cash
                    Cash = int(Cash - invest)
                      
                    ##display user equit
                    Equity_String = "You own {} share(s) of {} Congratulations!".format(Shares,Stonk)
    
                    ##display remaining investable cash
                    Cash_String = "you have ${} left to invest".format(Cash)
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
                    print('You dont have enough money.')
                    ## start loop over 
                    continue
                    

def portload(UserID):
    Port_Data = purchaseinfo(UserID)    
    
    Port_load = "INSERT INTO Portfolio (UserID, date_time, stonks, shares, cost, mkt_price, total_val, cash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"   
    for x, data in enumerate(Port_Data):
        mycursor.execute(Port_load, data)
    db.commit()
    
    
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
        Equity = total_shares * Market
        
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
        avg_cost = Cost / total_shares
        #Profit by stock = total Current equity - Total intitial investment cost
        profit = Equity - Cost
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
    print("\nBalance: ${:0.2f}\nProfit/Loss: ${:0.2f}\nPecent Return: {:0.4f}%".format(Balance, Profit, Return))


# def sell(UserID):
    
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

