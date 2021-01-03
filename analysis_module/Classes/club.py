class Club:
    members=[]
    def __init__(self, name ):
        self.name = name

    def add_member(self, member):
        self.members.append(member)

    def fetch_members(self):
        return self.members

    def insert_list(self):
        output = ""
        for mem in self.members:
            output = str(output+","+mem)
        return output

