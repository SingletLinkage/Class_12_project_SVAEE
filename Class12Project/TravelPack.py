class Pack:
    src = ''
    dest = ''
    desc = ''
    cost = ''
    id = ''
    name = ''

    def __init__(self, src, dest, desc, cost, pack_id, name):
        self.src = src
        self.dest = dest
        self.desc = desc
        self.cost = cost
        self.id = pack_id
        self.name = name
