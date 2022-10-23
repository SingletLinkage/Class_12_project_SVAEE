from User import *
from Helper import *
import sys
import HomePage

currentUser: User = None


def init(user: User):
    global currentUser
    currentUser = user

    welcome()


def welcome():
    print('-' * 70)
    print('User Profile'.center(70, '-'))
    print('-' * 70)
    view_details()
    next_action()


def view_details():
    print(f'Username: {currentUser.username} -- {currentUser.type}')
    print(f'First Name: {currentUser.first_name}')
    print(f'Last Name: {currentUser.last_name}')
    print(f'Password: {currentUser.password}')
    print(f'Packs Active: {len(currentUser.active_packs)}')


def next_action():
    # asking user for activity
    print('What do you want to do ?')
    print('1. View your Travel Packs')
    print('2. Cancel a Travel Pack')
    print('3. Go back to Home Page')
    print('4. Quit')

    # input validator
    choice = -1
    while (choice := input()) not in ['1', '2', '3', '4']:
        print('Please choose a valid option')

    # routing control as per user choice
    if choice == '1':
        view_user_packs()
    elif choice == '2':
        cancel_pack()
    elif choice == '3':
        go_home()
    elif choice == '4':
        sys.exit()


def go_home():
    HomePage.init(currentUser)


def view_user_packs():
    user_pack_ids = currentUser.active_packs
    if len(user_pack_ids) > 0:
        req_str = ",".join([str(i) for i in user_pack_ids])
        packs = get_data_from_table(f'select * from pack_details where id in ({req_str});')
    else:
        packs = 'You do not have any current active packs'
    print(packs)
    print('\n' * 2)
    next_action()


def cancel_pack():
    id = int(input('Enter id of Travel Package: '))

    if id not in currentUser.active_packs:
        print('You don\'t have the pack in your account')
    else:
        user_delpack(id)
        print('Deleted the pack from your account successfully')
    print('\n' * 2)
    next_action()


def user_delpack(id):
    global currentUser
    currentUser.delpack(id)


if __name__ == '__main__':
    welcome()
