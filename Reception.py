import socket, json
from TakeInput import TakeInput
from DatabaseManager import DatabaseManager
from PasswordEncryptor import PasswordEncryptor
from Capture import Capture
from Recognise import Recognise

class Reception:

    __dbManager = None
    
    def main(self):

        self.__dbManager = DatabaseManager()
        
        print('')
        print('Welcome to our library! What would you like to do? Please enter the number of option.')
        print('1. Sign up a new account')
        print('2. Log in with Password')
        print('3. Log in with Facial Recognition')
        print('4. Exit')

        option = TakeInput.inputInteger(1,4)

        if option == 1:
            self.register()
        elif option == 2:
            self.loginWithPassword()
        elif option == 3:
            self.loginWithFacial()
        else:
            self.logout()
    
    def register(self):

        userName = TakeInput.inputString('Please enter your username, username must have at least 4 characters, 16 characters maximum.','username')       
        while(self.__dbManager.checkUsername(userName) == False):

            print('Username exists, Please use another one.')
            
            userName = TakeInput.inputString('Please enter your username, username must have at least 4 characters, 16 characters maximum.','username')

        firstName = TakeInput.inputString('Please enter your first name, must not contain spaces or symbols, at least 2 characters long.', 'name')
        lastName = TakeInput.inputString('Please enter your last name, must not contain spaces or symbols, at least 2 characters long.', 'name')
        email = TakeInput.inputString('Please enter your email address.', 'email')
        password = TakeInput.inputString('Please enter your password, at least 6 characters long, maximum 16 characters', 'password')
        hashedPassword = PasswordEncryptor.hashPassword(password)

        self.__dbManager.insertData(userName, firstName, lastName, email, hashedPassword)
        
        self.takePicture(userName)
        print('Thank you for joining us! Your account has been created, you can login now!')
        
        self.main()
    
    def takePicture(self, userName):
        
        capture = Capture()
        capture.main(userName)      
        
    def loginWithPassword(self):
 
        userName = TakeInput.inputString('Please enter your user name: ', 'username')
        password = TakeInput.inputString('Please enter your password: ', 'password')
        
        if (self.__dbManager.validateLogin(userName, password) == False):
            self.main()
        else:
            self.establishConnection(userName)
    
    def loginWithFacial(self):
        
        userName = Recognise.recognisePerson()   
    
        if (userName == 'Unknown'):
            self.main()
        else:
            self.establishConnection(userName)

    def establishConnection(self, userName):
        
        HOST = ""
        with open('MasterIP.json','r') as ipFile:
            values = json.load(ipFile)
            HOST = values['master']
            
        PORT = 9876
        ADDRESS = (HOST,PORT)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to Master Pi as " + userName + '...')
            s.connect(ADDRESS)
            print("Connected.")
            s.sendall(userName.encode())
            print("Master Pi application in progressing...")
            
            while True:
                data = s.recv(4096)                
                if data.decode() == 'logout':                  
                    self.logout()
        
    def logout(self):
        
        print("Thank you for coming to our library, thank you!")
   
if __name__ == "__main__":
        
    re = Reception()
    
    re.main()
    