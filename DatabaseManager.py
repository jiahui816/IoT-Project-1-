import sqlite3, operator
from PasswordEncryptor import PasswordEncryptor

class DatabaseManager:

    __connection = 0
    __cursor = 0    

    def __init__(self):
        
        self.__connection = sqlite3.connect('users.db')

        self.__cursor = self.__connection.cursor()
                
        self.createTable()

    def createTable(self):

        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS USER
                (ID INTEGER PRIMARY KEY,
                    USERNAME       TEXT,
                    FIRSTNAME      TEXT,
                    LASTNAME       TEXT,
                    EMAIL           TEXT,
                    PASSWORD        VARCHAR(200));''')

        self.__connection.commit()

    def insertData(self, userName, firstName, lastName, email, password):

        self.__cursor.execute("INSERT INTO USER VALUES (NULL, ?, ?, ?, ?, ?)",(userName, firstName, lastName, email, password))
        self.__connection.commit()
        
    def checkUsername(self, userName):

        self.__cursor.execute('SELECT USERNAME FROM USER;')

        data = self.__cursor.fetchall()

        allUserNames = []

        for userNameTuple in data:
            allUserNames.append(userNameTuple[0])
                
        for user in allUserNames:
            if userName == user:
                return False
                    
        return True
                
        
    def validateLogin(self, userName, password):
            
        userNotExists = self.checkUsername(userName)
                
        if userNotExists == True:
            print("User name does not exist! please try again.")
                
            return False
                
        self.__cursor.execute("SELECT PASSWORD FROM USER WHERE USERNAME = ?;",(userName,))
                
        data = self.__cursor.fetchone()
            
        DBPassword = data[0]

        if not PasswordEncryptor.verifyPassword(password, DBPassword):
            print("Username and password does not match please try again!")
            return False
        else:
            print("Welcome! " + userName + " You are now logged in!")
            return True
