# Landing Page of 'Daily Travel Management system'
# Users are supposed to run this page, other files will be loaded as per need


# importing required modules
# dotenv is an external module and needs to be downloaded before usage
from dotenv import load_dotenv
from base64 import b64encode
import os

# ei landing page take run korate hobe, Log in take noy
# halka document kora start kkroechi kintu ekdomy valo hoyni


# shows welcome message
def greet():
    print('-' * 70)
    print('SETUP PAGE'.center(70, '-'))
    print('-' * 70)


# sets up environment variables, if present previously
# if not, prompts to set up environment variables
def setup():
    load_dotenv()
    if os.getenv('PASSWORD') is None:
        get_data()

    from Login import welcome
    welcome()


# prompts user to enter login credentials for the SQL Database, cals write() to save those credentials
def get_data():
    greet()
    print('For the application to run properly, your database credentials are needed')
    print('This will happen only for the first time this application is executed')

    username = input('Enter username for MySQL database: ')
    password = input('Enter the password: ')
    database_name = input('Enter the name of the database: ')
    write(username, password, database_name)


# saves the login credentials with base64 encoding
def write(username, pwd, database_name):
    with open('.env', 'w') as file:
        file.write(f'USER = {to_b64(username)}\nPASSWORD = {to_b64(pwd)}\nDATABASE = {to_b64(database_name)}')


# encodes in base64 format
def to_b64(p):
    return b64encode(p.encode('ascii')).decode('ascii')


setup()
