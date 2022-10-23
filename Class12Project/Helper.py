import pandas as pd
import mysql.connector


def execute_sql(query):
    # actually for executing general query -- DOES NOT return anything
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='lel im not giving it here',
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
        passwd='sem as abv',
        database='IPproject_test'
    )

    if conn.is_connected():
        return pd.read_sql(query, conn)
    else:
        print('Could not connect to sql database')

    conn.close()
