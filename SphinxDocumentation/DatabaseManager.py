class DatabaseManager:
    'This class implement the database connection.'
    __connection = 0
    __cursor = 0    

    def __init__(self):
        '''
        This function is used to connect to the database.
            Args:
                param1:Current Object
        '''
        
        self.__connection = sqlite3.connect('users.db')

        self.__cursor = self.__connection.cursor()
                
        self.createTable()

    def createTable(self):
        '''
        This function is used to create a user information's table.
            Args:
                param1:Current Object
        '''

        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS USER
                (ID INTEGER PRIMARY KEY,
                    USERNAME       TEXT,
                    FIRSTNAME      TEXT,
                    LASTNAME       TEXT,
                    EMAIL           TEXT,
                    PASSWORD        VARCHAR(200));''')

        self.__connection.commit()

    def insertData(self, userName, firstName, lastName, email, password):
        '''
        This function is used to insert user's details.
            Args:
                param1:Current Object

                param2:User name

                param3:User first name

                param4:User last name

                param5:User email

                param6:User password
        '''

        self.__cursor.execute("INSERT INTO USER VALUES (NULL, ?, ?, ?, ?, ?)",(userName, firstName, lastName, email, password))
        self.__connection.commit()
        
    def checkUsername(self, userName):
        '''
        This function is used to check user name.
            Args:
                param1:Current Object

                param2:User name
            
            Returns:
                Return the boolean value
        '''
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
        '''
        This function is used to valid the user login information.
            Args:
                param1:Current Object

                param2:User name

                param3:User password
            
            Returns:
                Return the boolean value
        '''
            
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
