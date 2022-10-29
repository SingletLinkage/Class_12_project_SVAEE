from Helper import execute_sql, get_data_from_table


# User class - helps to organise the data and provides a better way to transfer data from one page to the other
class User:
    first_name = ''
    last_name = ''
    username = ''
    password = ''
    type = ''  # ADMIN or CUSTOMER
    active_packs = []  # list of pack ids (integer list)

    def __init__(self, username, password, first_name=' ', last_name=' ', rank='CUSTOMER', packs=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.type = rank

        # if the user is initialised with no packs, load active_packs from database
        if packs is None:
            self.load_packs()
        else:
            self.active_packs = packs

    # adds a pack to user account using pack id
    def addpack(self, id):
        self.active_packs.append(id)
        self.update_active_packs()

    # deletes a pack from user account using pack id
    def delpack(self, id):
        self.active_packs.remove(id)
        self.update_active_packs()

    # updates active_packs in the MySQL Database (table user_list)
    def update_active_packs(self):
        new_pack_str = ','.join([str(i) for i in self.active_packs])
        query = f'update user_list set active_packs = "{new_pack_str}" where username = "{self.username}";'
        execute_sql(query)

    # loads active_packs from the MySQL Database (table user_list)
    def load_packs(self):
        packs = get_data_from_table(
            f'select active_packs from user_list where username="{self.username}";').active_packs.values[0]
        if packs == ' ' or packs == '':
            self.active_packs = []
        else:
            self.active_packs = [int(i) for i in packs.split(',')]
