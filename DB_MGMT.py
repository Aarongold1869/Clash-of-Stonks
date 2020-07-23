# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:59:05 2020

@author: Aaron Goldstein
"""

import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "stonkdb"
    )

mycursor = db.cursor()



## describe mysql table(s) in stonkdb
def describetable():
    mycursor.execute("DESCRIBE User")
    for x in mycursor: 
        print(x)

## print mysql table(s) in stonkdb
def printtables():
    # mycursor.execute("SELECT * FROM Portfolio")
    # for x in mycursor:
    #     print(x,"\n")
        
    mycursor.execute("SELECT * FROM Orders")
    for x in mycursor:
        print(x)
        
    mycursor.execute("SELECT * FROM User")
    for x in mycursor:
        print(x,"\n")
    
    mycursor.execute("SELECT * FROM Stocks")
    for x in mycursor:
        print(x)
    
    # mycursor.execute("SELECT * FROM Awards")
    # for x in mycursor:
    #     print(x)
        
    # mycursor.execute("SELECT * FROM Award_descriptions")
    # for x in mycursor:
    #     print(x)
        
    # mycursor.execute("SELECT * FROM Suggestions")
    # for x in mycursor:
    #     print(x,"\n")

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
    mycursor.execute("TRUNCATE table stonkdb.Orders") 
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


# mycursor.execute("UPDATE User SET cash = 200000.00 WHERE UserID = 1")
# db.commit()
# trunkuser()
printtables()
# describetable()


