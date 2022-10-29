from User import *
from Helper import *
import sys
import UserProfile

# each currentUser will be an object of User class. This is used to just simplify things when code grows
currentUser: User = None
all_packs = None


# reloads packs from database and stores them in all_packs DataFrame
def init_packs():
    global all_packs
    all_packs = get_data_from_table('select * from pack_details;')


# recieves an instance of User class and stores it in currentUser
def init(user: User):
    global currentUser
    currentUser = user

    init_packs()
    welcome()


# displays a welcome message
def welcome():
    print('HOME PAGE'.center(70, '-'))
    msg = f'WELCOME {currentUser.username}'
    print(msg.center(70, '-'))
    print('-' * 70)
    next_action()


# general prompt to get next user action
def next_action():
    # asking user for activity
    print('-' * 70)
    print('What do you want to do ?')
    print('1. View all Travel Packs')
    print('2. Book a Travel Pack')
    print('3. View My Account')
    print('4. Quit')

    # input validator
    choice = -1
    while (choice := input()) not in ['1', '2', '3', '4']:
        print('Please choose a valid option')

    # routing control as per user choice
    if choice == '1':
        view_packs()
    elif choice == '2':
        book_pack()
    elif choice == '3':
        visit_profile()
    elif choice == '4':
        sys.exit()


# displays all current available packs
def view_packs():
    print('-' * 70)
    print(all_packs.to_string())
    print('-' * 70)
    next_action()


# "book"s a pack (places it in user's active_packs field
def book_pack():  # Payment yet to be incorporated
    id = int(input('Enter id of Travel Package: '))
    if id not in all_packs.id.values:
        print('Invalid id, no such package exists')
    elif id in currentUser.active_packs:
        print('You already have the pack in your account')
    else:
        user_addpack(id)
        print('Added pack to your account successfully')
    next_action()


# transfers user to their profile page
def visit_profile():
    add_delay()
    UserProfile.init(currentUser)


# helper method to add a pack to user account
def user_addpack(id):
    global currentUser
    payment()
    currentUser.addpack(id)
