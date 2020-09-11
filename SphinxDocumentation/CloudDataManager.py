class CloudDataManager:
    'This class show the details of the implementation of cloud database.'
    HOST = "35.201.13.47"
    USER = "root"
    PASSWORD = "Felix19961213"
    DATABASE = "LMS"

    def __init__(self, connection = None):
        '''
        This function is used to connect to the database.
           Args:
            param1:Current Object

            param2:Creat connection
        '''
        
        if(connection == None):
            connection = MySQLdb.connect(CloudDataManager.HOST, CloudDataManager.USER,
                CloudDataManager.PASSWORD, CloudDataManager.DATABASE)
        self.connection = connection
        
    def close(self):
        '''
        This function is used to close to the database connection.
           Args:
            param1:Current Object
        '''
        self.connection.close()

    def checkLmsUserTable(self):
        '''
        This function is used to create a User table if not exists in Lms.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists LmsUser (
                    LmsUserID int not null auto_increment,
                    UserName nvarchar(256) not null,
                    Name text not null,
                    constraint PK_LmsUser primary key (LmsUserID),
                    constraint UN_UserName unique (UserName)
                )""")
            
        self.connection.commit()
        
    def checkBookTable(self):
        '''
        This function is used to check and create a Book table if not exists.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Book (
                    BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    PublishedDate date not null,
                    constraint PK_Book primary key (BookID)
                )""")
           
        self.connection.commit()
    
    def checkBookStatus(self,bookID):
        '''
        This function is used to check the selected book' status.
           Args:
            param1:Current Object

            param2:Book ID
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select BookID from BookBorrowed where Status = 'borrowed' and BookID = %s", (bookID,))
            result = cursor.fetchall()     
        if len(result) == 0:
            return True
        else:
            return False

    def checkBookBorrowedTable(self):
        '''
        This function is used to check a table for books have been borrowed.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists BookBorrowed (
                    BookBorrowedID int not null auto_increment,
                    LmsUserID int not null,
                    BookID int not null,
                    Status enum ('borrowed', 'returned'),
                    BorrowedDate date not null,
                    ReturnedDate date null,
                    constraint PK_BookBorrowed primary key (BookBorrowedID),
                    constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references
                LmsUser (LmsUserID),
                    constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
                )""")
        self.connection.commit()
    
    def insertLmsUser(self, userName, name):
        '''
        This function insert user name and name into User table.
           Args:
            param1:Current Object

            param2:The current user name

            param3:Name
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("insert into LmsUser (UserName, Name) values (%s, %s)", (userName, name))
        self.connection.commit()

    def getAllUser(self):
        '''
        This function is used to receive users' information.
           Args:
            param1:Current Object
        '''
        result = None
        with self.connection.cursor() as cursor:
            cursor.execute("select LmsUserID, UserName, Name from LmsUser")
            result = cursor.fetchall()
            for record in result:
                print(record)
    
    def getAllBook(self):
        '''
        This function is used to get books' information.
           Args:
            param1:Current Object
        '''
        result = [""]
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Book")
            result = cursor.fetchall()
            
        if len(result) == 0:
            print("No result fouond!")
        else:
            print('{:>20}{:>20}{:>20}{:>20}'.format('ISBN','Title','Author', 'Published Date'))
            for row in result:
                print('{:>20}{:>20}{:>20}{:>20}'.format(row[0],row[1],row[2],str(row[3])))


    def searchBook(self, dataType,data):
        '''
        This function is used to serch the current existed book in database.
           Args:
            param1:Current Object

            param2:Data Type of the serched book

            param3:book's data
        '''
        result = [""]
        
        with self.connection.cursor() as cursor:
            
            if(dataType == "Title"):
                cursor.execute("select * from Book where Title = %s" , (data,))
                result = cursor.fetchall()
            elif(dataType == "ISBN"):
                cursor.execute("select * from Book where BookID = %s" , (data,))
                result = cursor.fetchall()
            elif(dataType == "Author"):
                cursor.execute("select * from Book where Author = %s" , (data,))
                result = cursor.fetchall()
            else:
                print("Column Name does not exist, please check again!")
        
        if len(result) == 0:
            print("No result fouond! Please check your input again!")
            
        else:
            print('{:>20}{:>20}{:>20}{:>20}'.format('ISBN','Title','Author', 'Published Date'))
            for row in result:
                print('{:>20}{:>20}{:>20}{:>20}'.format(row[0],row[1],row[2],str(row[3])))
                if len(result) == 1:
                    return len(result), row[0]
        
        return len(result),0
    
    def insertBookBorrowed(self, lmsUserID, bookID,borrowDate, eid):
        '''
        This function is used to record the books borrowed by user.
           Args:
            param1:Current Object

            param2:User Id in lms

            param3:Borrowed book ID

            param3:Borrowed date

            param4:Google calendar event ID
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("insert into BookBorrowed(LmsUserID, BookID, Status, BorrowedDate, EID) values (%s, %s, 'borrowed', %s, %s)", (lmsUserID, bookID,borrowDate,eid))
        self.connection.commit()
    
    def getBookQuantity(self):
        '''
        This function is used to get the selected books' quantity.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select count(BookID) from Book")
            result = cursor.fetchall()
        return result[0][0]
    
    def getBookName(self,bookID):
        '''
         This function is used to get book's name.
           Args:
            param1:Current Object

            param2:Book ID
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select Title from Book where BookID = %s",(bookID,))
            result = cursor.fetchall()
        return result[0][0]
    
    def getUserID(self,userName):
        '''
         This function is used to get user's ID.
           Args:
            param1:Current Object

            param2:User name
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select LmsUserID from LmsUser where UserName = %s",(userName,))
            result = cursor.fetchall()
        return result[0][0]
    
    def printABookDetail(self, bookID):
        '''
         This function is used to print book's information.
           Args:
            param1:Current Object

            param2:Book ID
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Book where BookID = %s",(bookID,))
            result = cursor.fetchall()
        
        print('{:>20}{:>20}{:>20}{:>20}'.format('ISBN','Title','Author', 'Published Date'))
        for row in result:
            print('{:>20}{:>20}{:>20}{:>20}'.format(row[0],row[1],row[2],str(row[3])))


    
    def getBookID(self,bookName):
        '''
         This function is used to get book's ID.
           Args:
            param1:Current Object

            param2:Book Name
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select BookID from Book where Title = %s",(bookName,))
            result = cursor.fetchall()
        return result[0][0]
    
    def getAllBookIdListUserBorrowed(self,userName):
        '''
         This function is used to list the books ID which are borrowed by User.
           Args:
            param1:Current Object

            param2:User Name
        '''
        userID = self.getUserID(userName)
        bookIdList = []
        with self.connection.cursor() as cursor:
            cursor.execute("select BookID from BookBorrowed where LmsUserID = %s and Status = 'borrowed'", (userID,))
            result = cursor.fetchall()
        for record in result:
            bookIdList.append(record[0])
            
        return bookIdList
    
    def getEid(self, userName, bookId):
        '''
         This function is used to get book's name.
           Args:
            param1:Current Object

            param2:User name

            param3:Book ID
        '''
        userId = self.getUserID(userName)
        with self.connection.cursor() as cursor:
            cursor.execute("select EID from BookBorrowed where Status = 'borrowed' and LmsUserID = %s and BookID = %s", (userId, bookId) )
            result = cursor.fetchall()
        return result[0][0]
    
    def returnBook(self,eId,returnDate):
        '''
         This function is used to update the books' information that had been returned.
           Args:
            param1:Current Object

            param2:Google calendar event ID

            param3:Book returned date
        '''
        
        with self.connection.cursor() as cursor:
            cursor.execute("update BookBorrowed set Status = 'returned' where EID = %s",(eId,))
            cursor.execute("update BookBorrowed set ReturnedDate = %s where EID = %s",(returnDate,eId))
        self.connection.commit()
    
        
