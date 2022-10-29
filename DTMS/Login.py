import Admin
from Helper import get_data_from_table, add_delay
from User import User
import sys
import HomePage
import Signup

users = None  # a pandas DataFrame
usernames: list = None
passwords: list = None


# takes values from user_list table and assigns those to the users DataFrame
def init_users():
    global users, usernames, passwords
    users = get_data_from_table('select * from user_list')
    usernames = users.username.values
    passwords = users.password.values


# shows welcome message
def welcome():
    init_users()
    print('-' * 70)
    print('LOGIN PORTAL'.center(70, '-'))
    print('-' * 70)
    check_user()


# checks if an user has an account alreday
def check_user():
    print('Do you already have an account? Enter y/n')
    choice = -1
    # for validating user input
    while (choice := input().lower()) not in ['y', 'n', 'yes', 'no']:
        if choice == 'exit' or choice == 'quit':
            sys.exit()
        print('Enter a valid choice')

    if choice == 'y' or choice == 'yes':
        next_action()
    else:
        add_delay()
        Signup.welcome()


# to log in user
def next_action():
    usrnem = input('Enter your username: ')
    pwd = input('Enter your password: ')

    if validate(usrnem, pwd):
        print('Login successful...')
        new_user = setup_user(usrnem)  # a new_user a an User type object

        # redirect user as per rank
        if new_user.type == 'CUSTOMER':
            add_delay()
            HomePage.init(new_user)
        elif new_user.type == 'ADMIN':
            add_delay()
            Admin.init(new_user)

    else:
        print('Heading you back to login portal...')
        print('-'*70)
        next_action()


# checks if username is present in database and correctly matches corresponding password
def validate(usrnem, pwd):
    if usrnem not in usernames:
        print('Username not found in database')
        return False
    else:
        idx = list(usernames).index(usrnem)
        if passwords[idx] != pwd:
            print('Incorrect password')
            return False
        else:
            return True


# takes user details from the database and sets up and returns an User type object
def setup_user(username):
    idx = list(usernames).index(username)
    password = passwords[idx]
    firstname = users.first_name.values[idx]
    lastname = users.last_name.values[idx]
    rank = users.type.values[idx]

    user = User(username, password, firstname, lastname, rank)
    return user
