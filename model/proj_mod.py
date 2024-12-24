
from sys import maxsize


class Proj:
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        #self.id = id

    # метод который выдаёт текстовое или строковое представление сущности к которой применяется
    def __repr__(self):
        return "%s" % (self.name)

    def __eq__(self, other):
        return self.name == other.name
        #return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

#    def id_or_max(self):
#        if self.id:
#            return int(self.id)
#        else:
#            return maxsize
