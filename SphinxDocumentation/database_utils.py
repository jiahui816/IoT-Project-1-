class DatabaseUtils:
    ''
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
        print("connection")
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection
        print("connected")
    def close(self):
        '''
        This function is used to close to the database connection.
           Args:
            param1:Current Object
        '''
        self.connection.close()

    def __enter__(self):

        return self

    def __exit__(self, type, value, traceback):

        self.close()

    def createLmsUserTable(self):
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
        
    def createBookTable(self):
        '''
        This function is used to create a Book table if not exists.
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

    def createBookBorrowedTable(self):
        '''
        This function is used to create a table for books have been borrowed.
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
    
    def insertLmsUser(self, name):
        '''
        This function insert user name and name into User table.
           Args:
            param1:Current Object

            param2:Name
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("insert into LmsUser (LmsUserID) values (%s)", (LmsUserID))
        self.connection.commit()

        return cursor.rowcount == 1

    def getUser(self):
        '''
        This function is used to get user's information.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select LmsUserID, UserName from LmsUser")
            return cursor.fetchall()

    def deleteUser(self, personID):
        '''
        This function is used to delete user ID.
           Args:
            param1:Current Object

            param2:Person ID
        '''
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from LmsUser where LmsUserID != %s", (LmsUserID))
        self.connection.commit()
        
    def insertBook(self, title, author, publishedDate):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Book (Title, Author, PublishedDate) values (%s,%s,%s)", (title, author, publishedDate))
        self.connection.commit()



    def searchBook(self, dataType,data):
        '''
        This function is used to serch the current existed book in database.
           Args:
            param1:Current Object

            param2:Data Type of the serched book

            param3:book's data
        '''
        result = ("")
        with self.connection.cursor() as cursor:
            if(dataType == "Title"):
                cursor.execute("select BookID,Title from Book where Title = %s " , (data,))
                result = cursor.fetchall()
            elif(dataType == "ISBN"):
                cursor.execute("select BookID,Title from Book where BookID = %s " , (data,))
                result = cursor.fetchall()
            elif(dataType == "Author"):
                cursor.execute("select BookID,Title from Book where Author = %s " , (data,))
                result = cursor.fetchall()
            else:
                print("Column Name does not exist, please check again!")
            
  
            for row in result:
                print(row)


    def deleteBook(self, bookID):
        '''
        This function is used to delete book in database.
           Args:
            param1:Current Object

            param2:Book ID
        '''
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Book where BookID != %s", (BookID,))
        self.connection.commit()
        
    def insertBookBorrowed(self, bookBorrowed):
        '''
        This function is used to insert the information of borrowed books.
           Args:
            param1:Current Object

            param2:Books have been borrowed
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("insert into BookBorrowed(BookBorrowedID) values (%s)", (LmsUserID,))
        self.connection.commit()

        return cursor.rowcount == 1

    def getBookBorrowed(self):
        '''
        This function is used to get borrowed book ID.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select BookBorrowedID from BookBorrowed")
            return cursor.fetchall()

    def deleteBookBorrowed(self, bookBorrowedID):
        '''
        This function is used to delete borrowed book ID.
           Args:
            param1:Current Object
        '''
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from BookBorrowed where BookBorrowedID != %s", (BookBorrowedID,))
        self.connection.commit()
        
if __name__=="__main__":
    db = DatabaseUtils()
    

    db.searchBook("Title","One Piece Vol 2")
    db.searchBook("ISBN","5")
    db.searchBook("Author","Eiichiro Oda")
    db.searchBook("jfch","ajkdjif")
    
    print('mmm')