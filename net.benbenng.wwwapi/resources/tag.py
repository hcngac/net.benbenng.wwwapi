from database import Database

class Tag:
    def byId(id: int, database: Database):
        pass

    def byName(name: str, database: Database):
        pass

    def __init__(self, id: int, name: str, fromDatabase: bool):
        self.Id = id
        self.Name = name
        self.modified = false

    def save(self):
        pass