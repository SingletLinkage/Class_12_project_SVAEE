from Helper import execute_sql, get_data_from_table


class User:
    first_name = ''
    last_name = ''
    username = ''
    password = ''
    type = ''  # ADMIN or CUSTOMER
    active_packs = []  # list of ids (int array)

    def __init__(self, username, password, first_name=' ', last_name=' ', rank='CUSTOMER', packs=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.type = rank

        if packs is None:
            self.load_packs()
        else:
            self.active_packs = packs

    def addpack(self, id):  # Payment yet to be incorporated
        self.active_packs.append(id)
        self.update_active_packs()

    def delpack(self, id):
        self.active_packs.remove(id)
        self.update_active_packs()

    def update_active_packs(self):
        new_pack_str = ','.join([str(i) for i in self.active_packs])
        query = f'update user_list set active_packs = "{new_pack_str}" where username = "{self.username}";'
        execute_sql(query)

    def load_packs(self):
        packs = get_data_from_table(
            f'select active_packs from user_list where username="{self.username}";').active_packs.values[0]
        if packs == ' ' or packs == '':
            self.active_packs = []
        else:
            self.active_packs = [int(i) for i in packs.split(',')]
