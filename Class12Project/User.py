from Helper import execute_sql


class User:
    first_name = ''
    last_name = ''
    username = ''
    password = ''
    type = ''  # ADMIN or CUSTOMER
    active_packs = []  # list of ids (int array)

    def __init__(self, username, password, first_name=' ', last_name=' ', rank='CUSTOMER', packs=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.type = rank
        self.active_packs = packs

    def addpack(self, id):
        self.active_packs.append(id)
        new_pack_str = ','.join([str(i) for i in self.active_packs])
        query = f'update user_list set active_packs = "{new_pack_str}" where username = "{self.username}";'
        execute_sql(query)
