import HomePage
from Helper import *
import sys
from User import User

users = None
all_packs = None
cur_user: User = None


# accepts an instance of User class and stores it in cur_user
def init(user):
    global cur_user
    cur_user = user
    welcome()


# reloads users from the MySQL database (from table user_list)
def init_users():
    global users
    users = get_data_from_table('select * from user_list;')


# reloads packs from the MySQL database (from table pack_details)
def init_packs():
    global all_packs
    all_packs = get_data_from_table('select * from pack_details;')


# displays guidelines for creating new packs
def view_guidelines():
    # would be changed later
    print('name, src, and dest can not be more than 20 characters in length')
    print('description should be less than 200 characters')


# shows the welcome message
def welcome():
    init_users()
    init_packs()
    print('-' * 70)
    print('ADMIN PORTAL'.center(70, '-'))
    print('-' * 70)
    next_action()


# general prompt to get next user action
def next_action():
    # asking admin for activity
    print('-' * 70)
    print('What do you want to do ?')
    print('1. View all Travel Packs')
    print('2. Add a Travel Pack')
    print('3. Modify a Travel Pack')
    print('4. Delete a Travel Pack')
    print('5. View details of users')
    print('6. Add a new Admin')
    print('7. Remove an Admin')
    print('8. Visit Home Page')
    print('9. Quit')

    # input validator
    choice = -1
    while (choice := input()) not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        print('Please choose a valid option')

    # routing control as per user choice
    if choice == '1':          view_packs()
    elif choice == '2':        add_pack()
    elif choice == '3':        modify_pack()
    elif choice == '4':        del_pack()
    elif choice == '5':        view_users()
    elif choice == '6':        add_admin()
    elif choice == '7':        remove_admin()
    elif choice == '8':
        add_delay()
        HomePage.init(cur_user)
    elif choice == '9':        sys.exit()


# adds a pack to the database (table pack_details)
def add_pack():
    view_guidelines()
    print('Enter the pack id: ', end='')
    pack_id = 'kek'
    while (pack_id := int(input())) in all_packs.id.values:
        print('Pack already exists. Enter another id: ', end='')

    name = input('Enter the name of travel pack: ')
    src = input('Enter pack source: ')
    dest = input('Enter pack destination: ')
    description = input('Enter pack description: ')
    cost = int(input('Enter the cost of pack: '))

    execute_sql(f'insert into pack_details values ("{src}", "{dest}", "{description}", {cost}, "{name}", {pack_id})')
    print('Pack added successfully...')

    init_packs()
    next_action()


# modifies attributes of a pack (except pack id) in the database
def modify_pack():
    view_guidelines()
    print('Enter the pack id: ', end='')
    pack_id = 'kek'
    while (pack_id := int(input())) not in all_packs.id.values:
        print('Pack not found. Enter valid id: ', end='')

    print('What do you want to modify ?')
    print('1. Source')
    print('2. Destination')
    print('3. Description')
    print('4. Cost')
    print('5. Name')

    # input validator
    choice = -1
    while (choice := input()) not in ['1', '2', '3', '4', '5']:
        print('Please choose a valid option')

    new_value = input('Enter modified value: ')
    parameter = ['src', 'dest', 'description', 'cost', 'name'][int(choice) - 1]
    execute_sql(f'update pack_details set {parameter}="{new_value}" where id={pack_id}')
    print('Pack modified successfully...')

    init_packs()
    next_action()


# deletes a pack from he database
def del_pack():
    print('Enter the pack id: ', end='')
    pack_id = 'kek'
    while (pack_id := int(input())) not in all_packs.id.values:
        print('Pack not found. Enter valid id: ', end='')

    execute_sql(f'delete from pack_details where id="{pack_id}"')
    print('Pack deleted successfully...')

    init_packs()
    next_action()


# displays all packs from the database
def view_packs():
    print('=' * 70)
    print(all_packs.to_string())
    print('=' * 70)
    if len(all_packs) == 0:
        prompt_load_default()
    next_action()


# allows admins to load default packs if there are no pack present
def prompt_load_default():
    print('Do you want to load default packs? Enter y/n')
    choice = -1
    while (choice := input().lower()) not in ['y', 'n', 'yes', 'no']:
        if choice == 'exit' or choice == 'quit':
            sys.exit()
        print('Enter a valid choice')

    if choice == 'y' or choice == 'yes':
        load_default_packs()
        init_packs()


# displays user details
def view_users():
    print('=' * 70)
    print(users.loc[:, ['first_name', 'last_name', 'username', 'active_packs', 'type']].to_string())
    print('=' * 70)
    next_action()


# adds an user to the list of admins
# the user must be previously registered
def add_admin():
    print('Enter the username of that user: ', end='')
    username = None
    while (username := input()) not in users.username.values:
        print('That user does not exist in database... Enter valid username: ', end='')

    execute_sql(f'update user_list set type="ADMIN" where username="{username}"')
    print('Admin added successfully...')

    init_users()
    next_action()


# removes an user from admin post
# the user remains as a customer
def remove_admin():
    print('Enter the username of that user: ', end='')
    username = None
    while (username := input()) not in users.username.values:
        print('That user does not exist in database... Enter valid username: ', end='')

    execute_sql(f'update user_list set type="CUSTOMER" where username="{username}"')
    print('Admin removed successfully...')

    init_users()
    next_action()
