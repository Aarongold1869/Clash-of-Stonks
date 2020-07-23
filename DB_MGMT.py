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
def describe_table(table):
    mycursor.execute("DESCRIBE {}".format(table))
    for x in mycursor: 
        print(x)

## print mysql table(s) in stonkdb
def print_tables():
    mycursor.execute("SELECT * FROM User")
    for x in mycursor:
        print(x,"\n")
        
    mycursor.execute("SELECT * FROM Orders")
    for x in mycursor:
        print(x,'\n')
        
    mycursor.execute("SELECT * FROM Portfolio")
    for x in mycursor:
        print(x,"\n")
    
    mycursor.execute("SELECT * FROM Stocks")
    for x in mycursor:
        print(x,'\n')
    
    mycursor.execute("SELECT * FROM Equity")
    for x in mycursor:
        print(x,'\n')
        
    # mycursor.execute("SELECT * FROM Award_descriptions")
    # for x in mycursor:
    #     print(x,'\n')
        
    # mycursor.execute("SELECT * FROM Suggestions")
    # for x in mycursor:
    #     print(x,"\n")


## truncate User table
def trunk_table(table):
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("TRUNCATE TABLE {}".format(table)) 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close


def drop_table(table):
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("DROP TABLE {}".format(table)) 
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.close



trunk_table('')
# print_tables()


