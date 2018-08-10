from database import Database
from tag import Tag
from user import User

class Project:
    def getById(id: int, database: Database) -> Project:
        pass

    def searchByKeyword(keyword: str, database: Database) -> list:
        pass

    def getByTag(tag: Tag, database: Database) -> list:
        pass

    def getByAuthor(author: User, database: Database) -> list:
        pass

    def __init__(self):
        pass

    def save(self):
        pass