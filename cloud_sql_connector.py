import datetime

import os

from flask import Flask, render_template, request, Response
import sqlalchemy



import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='stonkdb')


app = Flask(__name__)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3306, debug=True)
  

def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }

    return init_tcp_connection_engine(db_config)
 


def init_tcp_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_tcp]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = "root"
    db_pass = ""
    db_name = "stonkdb"
    db_host = "127.0.0.1:3306"
    
    
    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        ),
        # ... Specify additional properties here.
        # [END cloud_sql_mysql_sqlalchemy_create_tcp]
        **db_config
        # [START cloud_sql_mysql_sqlalchemy_create_tcp]
    )
    # [END cloud_sql_mysql_sqlalchemy_create_tcp]

    return pool

db = init_connection_engine()

# mycursor = db.cursor(buffered=True)

def test():
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute("SELECT * FROM User")
        
        
test()       
        