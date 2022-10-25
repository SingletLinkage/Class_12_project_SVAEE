import pandas as pd
import mysql.connector
import time

DATABASE = 'ip_project'
USERNAME = 'root'
PASSWORD = 'root'


def execute_sql(query):
    # actually for executing general query -- DOES NOT return anything
    conn = setup_connection_to_database()
    cursor = conn.cursor()

    if conn.is_connected():
        cursor.execute(query)
        cursor.execute('commit;')
    else:
        print('Could not connect to sql database')

    conn.close()


def get_data_from_table(query):
    # actually for reading sql and returning output
    conn = setup_connection_to_database()

    if conn.is_connected():
        return pd.read_sql(query, conn)
    else:
        print('Could not connect to sql database')

    conn.close()


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


def setup_general_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user=USERNAME,
        password=PASSWORD,
    )

    return connection


def add_delay():
    print('-' * 70)
    for i in 'L O A D I N G . . .'.split(' '):
        print(i, end=' ')
        time.sleep(0.3)

    print()
    print('-' * 70)


def init_database(database_name):
    connection = setup_general_connection()
    cursor = connection.cursor()
    cursor.execute(f'create database if not exists {database_name};')
    cursor.execute(f'use {database_name};')
    cursor.execute('''
    create table pack_details(
        src varchar(10),
        dest varchar(10),
        description char(100),
        cost int,
        name varchar(10),
        id int(10) primary key);''')

    cursor.execute('''
    create table user_list(
        first_name varchar(10),
        last_name varchar(10),
        username varchar(20) primary key,
        password varchar(20),
        active_packs varchar(120),
        type varchar(10));''')
    cursor.execute('insert into user_list values("admin1", "admin1", "admin", "admin", "", "ADMIN");')
    cursor.execute('commit;')


def check_if_exists(database):
    connection = setup_general_connection()
    all_databases = pd.read_sql('show databases;', connection).Database
    return database.lower() in all_databases.values
