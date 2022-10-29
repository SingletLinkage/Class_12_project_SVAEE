import pandas as pd
import mysql.connector
import time
import os
from dotenv import load_dotenv
from base64 import b64decode

DATABASE = None
USERNAME = None
PASSWORD = None


# initialises login credentials for the database, these remain base64 encrypted outside the program
def setup_variables():
    global DATABASE, USERNAME, PASSWORD
    load_dotenv()

    DATABASE = from_b64(os.getenv('DATABASE'))
    USERNAME = from_b64(os.getenv('USER'))
    PASSWORD = from_b64(os.getenv('PASSWORD'))


# decodes a string from base64 encoding
def from_b64(p):
    return b64decode(p.encode('ascii')).decode('ascii')


# for executing general sql queries -- DOES NOT return anything
def execute_sql(query):
    conn = setup_connection_to_database()
    cursor = conn.cursor()

    if conn.is_connected():
        cursor.execute(query)
        cursor.execute('commit;')
    else:
        print('Could not connect to sql database')

    conn.close()


# for reading sql and returning the output as pandas DataFrames
def get_data_from_table(query):
    conn = setup_connection_to_database()

    if conn.is_connected():
        return pd.read_sql(query, conn)
    else:
        print('Could not connect to sql database')

    conn.close()


# sets up a python to MySQL connection (to a particular database)
def setup_connection_to_database():
    if not check_if_exists(DATABASE):
        init_database(DATABASE)

    connection = mysql.connector.connect(
        host='localhost',
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    return connection


# sets up a python to MySQL connection (NOT to a particular database)
def setup_general_connection():
    if USERNAME is None:
        setup_variables()

    connection = mysql.connector.connect(
        host='localhost',
        user=USERNAME,
        password=PASSWORD,
    )
    return connection


# adds a bit of delay for improving user experience
def add_delay():
    print('-' * 70)
    for i in 'L O A D I N G . . .'.split(' '):
        print(i, end=' ')
        time.sleep(0.3)

    print()
    print('-' * 70)


# creates the database and its tables if it is not present already
def init_database(database_name):
    connection = setup_general_connection()
    cursor = connection.cursor()
    cursor.execute(f'create database if not exists {database_name};')
    cursor.execute(f'use {database_name};')
    cursor.execute('''
    create table pack_details(
        src varchar(20),
        dest varchar(20),
        description varchar(200),
        cost int,
        name varchar(20),
        id int(10) primary key);''')

    cursor.execute('''
    create table user_list(
        first_name varchar(20),
        last_name varchar(20),
        username varchar(20) primary key,
        password varchar(20),
        active_packs varchar(120),
        type varchar(20));''')
    cursor.execute('insert into user_list values("admin1", "admin1", "admin", "admin", "", "ADMIN");')
    cursor.execute('commit;')


# checks if a database exists
def check_if_exists(database):
    if database is None:
        setup_variables()
        database = DATABASE

    connection = setup_general_connection()
    all_databases = pd.read_sql('show databases;', connection).Database
    return database.lower() in all_databases.values


# generates a payment prompt
def payment():
    card = input('Enter you card number: ')
    while not validate_card(card, 16):
        card = input('Enter a valid card number: ')

    cvv = input('Enter CVV: ')
    while not validate_card(cvv, 3):
        cvv = input('Enter valid cvv number: ')

    print('Payment successful')


# validates length and type of card, etc.
def validate_card(card, length):
    flag = False
    if len(card) == length:
        flag = True

    try:
        int(card)
    except ValueError:
        flag = False

    return flag


# loads default packs present in the default_packages.CSV file
def load_default_packs():
    df = pd.read_csv('default_packages.CSV')
    conn = setup_connection_to_database()
    cursor = conn.cursor()
    for i, j in df.iterrows():
        cursor.execute(
            f'insert into pack_details values ("{j.src}", "{j.dest}", "{j.description}", {j.cost}, "{j.pack_name}", {j.id});')
        cursor.execute('commit;')
