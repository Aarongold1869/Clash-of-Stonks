# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:16:17 2020

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

# mycursor.execute("CREATE TABLE User (userID int PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(45), last_name VARCHAR(45), age smallint UNSIGNED, email VARCHAR(45), phone VARCHAR(45), user_name VARCHAR(45))")
# mycursor.execute("CREATE TABLE Portfolio (portID int PRIMARY KEY AUTO_INCREMENT, userID int, FOREIGN KEY(userID) REFERENCES User(userID), date_time DATETIME, stonks VARCHAR(100), shares VARCHAR(100), cost VARCHAR(100), mkt_price VARCHAR(100), total_val int UNSIGNED, perc_port decimal UNSIGNED)")


# mycursor.execute("ALTER TABLE User ADD COLUMN date_time DATETIME")


# mycursor.execute("SET SQL_SAFE_UPDATES = 0")
# mycursor.execute("ALTER TABLE User DROP age")
# mycursor.execute("ALTER TABLE USER ADD DOB DATE AFTER last_name")
# mycursor.execute("SET SQL_SAFE_UPDATES = 1")

# for x in mycursor:
#     print(x)


# mycursor.execute("ALTER TABLE User_Balance MODIFY COLUMN percent_return DECIMAL(10,4)")
# db.close

# mycursor.execute("ALTER TABLE User ADD Rank INT NOT NULL AFTER p;")
# db.close


# UserID =1
# mycursor.execute("SELECT cash FROM Portfolio WHERE UserID ={} LIMIT 1".format(UserID))
# for x in mycursor:
#     Initial = x
    
# print(Initial )

# mycursor.execute("CREATE TABLE suggestions (sugID int PRIMARY KEY AUTO_INCREMENT, userID int, FOREIGN KEY(userID) REFERENCES User(userID), date_time DATETIME, award VARCHAR(45), description VARCHAR(300))")

























