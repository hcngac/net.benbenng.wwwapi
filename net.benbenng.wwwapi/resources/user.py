from database import Database
from cache import Cache
import hashlib
import uuid
import binascii
import datetime

class User:
    def getById(id: int, database: Database) -> User:
        try:
            rows = database.execute("SELECT * FROM Users WHERE Id=%s", (id,))
            if (len(row) == 0):
                raise Exception("User not found!")
            return rows[0]
        except e:
            raise e

    def getByLoginName(login_name: str, database: Database) -> User:
        try:
            rows = database.execute("SELECT * FROM Users WHERE LoginName=%s", (login_name,))
            if (len(row) == 0):
                raise Exception("User not found!")
            return rows[0]
        except e:
            raise e

    def getByEmail(email: str, database: Database) -> User:
        try:
            rows = database.execute("SELECT Id FROM UserInformation WHERE Email=%s", (email,))
            if (len(row) == 0):
                raise Exception("User not found!")
            row = rows[0]
            return getById(row[0])
        except e:
            raise e

    def getByToken(token: str, cache: Cache, database: Database) -> User:
        id = cache.redis.hget('tokens', token)
        if id is None:
            raise Exception("Token not registered.")
        id = int(id.decode('utf-8'))
        try:
            return getById(id, database)
        except e:
            raise e
        pass

    def hash_password(password: str, salt: str) -> str:
        hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8')[:128], salt.encode('utf-8')[:128], 100000)
        return binascii.hexlify(hash_password).decode("utf-8")

    def createUser(database: Database, login_name: str, password: str, role: str, email: str = "",first_name: str = "", last_name: str = "") -> User:
        try:
            salt = uuid.uuid4().hex
            hash_password = User.hash_password(password, salt)
            user_credentials = (login_name, hashed_password, salt, role)
            user_information = (email, first_name, last_name, datetime.datetime.now)
            database.execute("INSERT INTO Users (LoginName, HashedPassword, Salt, Role) VALUES (%s, %s, %s, %s)", user_credentials)
            database.commit()
            rows = database.execute("SELECT * FROM Users WHERE LoginName=%s", (login_name,))
            if rows is None or len(rows) == 0:
                raise Exception("New user cannot be added to database!")
            return User()
        except e:
            raise e
        pass

    def __init__(self, id: int, login_name: str, hashed_password: str, salt: str, role: str):
        self.id = id
        self.hashed_password = hashed_password
        self.salt = salt
        self.role = role

    def getUserInformation(self, database: Database) -> UserInformation:
        rows = database.execute("SELECT * FROM UserInformation WHERE Id=%s", (self.id,))
        if rows is None or len(rows) == 0:
            raise Exception("User Information not found!")
        row = rows[0]
        return UserInformation(*row)

    def changePassword(self, new_password: str, database: Database):
        self.hashed_password = hash_password(new_password, self.salt)
        database.execute("UPDATE Users SET HashedPassword = %s WHERE Id = %s", (self.hashed_password, self.id))

class UserInformation:
    def __init__(self, id, email, first_name, last_name, last_active_time):
        pass