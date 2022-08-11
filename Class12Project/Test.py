# importing required modules
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import mysql.connector as sqltor
import dotenv
import os

# loading environment variables
dotenv.load_dotenv()
_username = os.getenv('USERNAME')
_password = os.getenv('PASSWORD')
_database = os.getenv('DATABASE')

# creating required connections
conn = sqltor.connect(
    host='localhost',
    user=_username,
    passwd=_password,
    database=_database
)

engine = create_engine(f'mysql+pymysql://{_username}:{_password}@localhost/{_database}')
sql_connection = engine.connect()

# --------------- actual program starts here -------------------
if conn.is_connected():
    print('Connection successful')
    name = 'user2'
    query = 'select * from userinfo;'
    dataframe = pd.read_sql(query, conn)
    print(dataframe)

df = pd.read_csv('testing.csv', header=0)
print(df)
df.to_sql('newtable', sql_connection, if_exists='replace', index=False)

conn.close()
