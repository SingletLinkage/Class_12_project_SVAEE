from User import *
from Helper import *
import sys
import UserProfile

# each currentUser will be an object of User class. This is used to just simplify things when code grows
currentUser = User('firstone', 'pwd')

# dataframe containing all the packs
all_packs = get_data_from_table('select * from pack_details;')


# initialises user, ignore for now
def init(user: User):
    global currentUser
    currentUser = user

    welcome()


def welcome():
    print('HOME PAGE'.center(70, '-'))
    msg = f'WELCOME {currentUser.username}'
    print(msg.center(70, '-'))
    print('-' * 70)
    next_action()


def next_action():
    # asking user for activity
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


def view_packs():
    print(all_packs)
    print('\n' * 3)
    next_action()


def book_pack():  # Payment yet to be incorporated
    id = int(input('Enter id of Travel Package: '))
    if id not in all_packs.id.values:
        print('Invalid id, no such package exists')
    elif id in currentUser.active_packs:
        print('You already have the pack in your account')
    else:
        user_addpack(id)
        print('Added pack to your account successfully')
    print('\n' * 2)
    next_action()


def visit_profile():
    UserProfile.init(currentUser)


def user_addpack(id):
    global currentUser
    currentUser.addpack(id)


if __name__ == '__main__':
    welcome()
