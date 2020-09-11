import socket, time
from TakeInput import TakeInput
from CloudDataManager import CloudDataManager
from EventManager import EventManager
from datetime import datetime
from datetime import timedelta
from QrCode import QrCode
from VoiceSearch import VoiceSearch

class Master:
    
    def menu(self,userName):
        
        cdb = CloudDataManager()
        option = ""
        while(option != 4):
            print("")
            print("Welcome "+ userName +", what would you like to do?")
            print("0. View All Books")
            print("1. Search A Book")
            print("2. Borrow A Book")
            print("3. Return A Book")
            print("4. Logout")      
            option = TakeInput.inputInteger(0,4)
            
            if option == 0:
                cdb.getAllBook()
            elif option == 1:
                self.searchBook(userName,cdb)
            elif option == 2:
                self.borrowBook(cdb, userName)
            elif option == 3:
                self.returnBook(cdb, userName)
                
        cdb.close()
        return 4
        
    def searchBook(self, userName, cloudDB):
        print("In which way you want to search the Book:")
        print("1.Search by entering")
        print("2.Search by voice recognition")
        choose = TakeInput.inputInteger(1,2)
        
        if choose == 2:
            bookName = VoiceSearch.search()
            if bookName == None:
                return
            bookName = bookName.title()
            bookResultNum, bookId = cloudDB.searchBook('Title', bookName)
        else:
            searchType = TakeInput.inputBookSearchType()
            searchData = input('Please enter the search data:')
            bookResultNum, bookId = cloudDB.searchBook(searchType, searchData)
            
        opt = ""
        if bookResultNum == 1:
            print("Would you like to borrow this book?(Y/N)")
            opt = TakeInput.inputString("","choose")
            if opt == 'Y':
                self.borrowBook(cloudDB,userName,bookId)
        return
    
    def returnBook(self, cloudDB, userName):
        
        bookReturnList = cloudDB.getAllBookIdListUserBorrowed(userName)
        if len(bookReturnList) == 0:
            print("You don't have any book to return!")
        else:
        
            print("You can return book No:" + str(bookReturnList))
            for bookID in bookReturnList:
                cloudDB.printABookDetail(bookID)
            print("In which way you want to return the book?")
            print("1. Enter ID")
            print("2. Scan QR Code")
            
            option = TakeInput.inputInteger(1,2)
            if option == 1:            
                print("Which book you want to return?")
                bookId = int(input('Please input the book id you want to return:'))
                while ((bookId in bookReturnList) == False):
                    bookId = int(input("Book Id invalid, please re-enter:"))             
            else:
                print("Please place the book Qr Code infront of the web camera..")
                bookId = int(QrCode.scan())
                while ((bookId in bookReturnList) == False):
                    print("Invalid QrCode, please don't return the book you didn't borrow.")
                    return
                
                
            print("You are returning book No." + str(bookId))    
                
            eId = cloudDB.getEid(userName, bookId)               
            EventManager.deleteEvent(eId)
            returnDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cloudDB.returnBook(eId,returnDate)
            print('Book returned successfully! Thank you!')
        
        return
        
    def borrowBook(self, cloudDB, userName, bookID = -1):
        
        if bookID == -1:
            print('Please enter the ISBN number of the book you want to borrow:')
            bookID = TakeInput.inputInteger(1,cloudDB.getBookQuantity())
        availabale = cloudDB.checkBookStatus(bookID)
        if availabale == False:
            print("Sorry, this book is current not availabale, please borrow another one..")
        else:
            
            borrowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            returnDate = (datetime.now() + timedelta(days = 7)).strftime("%Y-%m-%d %H:%M:%S")          
            userID = cloudDB.getUserID(userName)           
            bookName = cloudDB.getBookName(bookID)
            eid = EventManager.insert(bookName,userName)
            
            print("")
            print('Book borrow detail')
            print("Borrow Date: "+borrowDate)
            print("Return Date: "+returnDate)
            print("Book detail:")
            cloudDB.printABookDetail(bookID)
            cloudDB.insertBookBorrowed(userID,bookID,borrowDate,eid)
            print("")
            print('Book Borrowed Successfull! Please return it within 7 days!')
            print("")
            
        return
        
    def connection(self):
        
        print("Waiting for connection from reception...")
                
        HOST = ""
        PORT = 7777
        ADDRESS = (HOST, PORT)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDRESS)
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(4096)
                    if data != "":
                        userName = data.decode()
                        if self.menu(userName) == 4:
                            msg = "logout"
                            conn.sendall(msg.encode())
                            break
            print("User log out!")

        

if __name__ == "__main__":
    
    ms = Master()
    ms.connection（）

