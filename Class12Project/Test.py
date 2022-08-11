# Demo for how to use the pymysql, sqlalchemy and mysql connector libraries
# Using environment variable (dotenv) not strictly necessary but allows you to not expose sensitive info like passwords in code files.
# Instead, you can separately create a .env file containing the USERNAME, PASSWORD and DATABASE variables.


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
# to know how this(^) works search 'python f strings', this is easier than string formatting using %s
sql_connection = engine.connect()

# --------------- actual program starts here -------------------
if conn.is_connected():
    print('Connection successful')
    query = 'select * from userinfo;'  # can be any valid sql statement
    dataframe = pd.read_sql(query, conn)
    print(dataframe)
else:
    print('Connection problem')
# above code reads from table userinfo into a pandas DataFrame 'dataframe' and prints it

df = pd.read_csv('testing.csv', header=0)
print(df)
df.to_sql('newtable', sql_connection, if_exists='replace', index=False)
# above block reads data from a csv file into a dataframe 'df' and then writes that into a sql table 'newtable'


# closing connections
conn.close()
