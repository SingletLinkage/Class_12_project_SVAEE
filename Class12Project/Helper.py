import pandas as pd
import mysql.connector
import time


def execute_sql(query):
    # actually for executing general query -- DOES NOT return anything
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='IPproject_test'
    )
    cursor = conn.cursor()

    if conn.is_connected():
        cursor.execute(query)
        cursor.execute('commit;')
    else:
        print('Could not connect to sql database')

    conn.close()


def get_data_from_table(query):
    # actually for reading sql and returning output
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='IPproject_test'
    )

    if conn.is_connected():
        return pd.read_sql(query, conn)
    else:
        print('Could not connect to sql database')

    conn.close()


def add_delay():
    print('-' * 70)
    for i in 'L O A D I N G . . .'.split(' '):
        print(i, end=' ')
        time.sleep(0.3)

    print()
    print('-' * 70)

