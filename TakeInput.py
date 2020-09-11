import re
class TakeInput:
  
    @staticmethod
    def inputString(msg, inputType):

        isValid = False
        info = input(msg)

        if inputType == 'ip':
            pattern = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        elif inputType == 'name':
            pattern = re.compile('[A-Za-z]{2,25}')
        elif inputType == 'email':
            pattern = re.compile('^[a-zA-Z\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
        elif inputType == 'username':
            pattern = re.compile('[A-Za-z0-9@#$%^&+=]{4,16}')
        elif inputType == 'password':
            pattern = re.compile('[A-Za-z0-9@#$%^&+=]{6,16}')
        elif inputType == 'choose':
            pattern = re.compile('^(?:Y|N)$')
    
        if(pattern.match(info)):
            isValid = True

        while(isValid == False):
            info = input("Invalid "+ inputType + " format. Please re-input: ")
            if(pattern.match(info)):
                isValid = True
                
        return info
    
    @staticmethod
    def inputInteger(min,max):     
        isValid = False
        
        while isValid == False:
            try:
                number = input("Please enter an integer number: ")
                number = int(number)              
                while (int(number) < min) or (int(number) > max):
                    number = int(input("Invalid number, please re-input: "))
                isValid = True
                
            except ValueError:
                print("Please input an integer!")
            
        return number
    
    @staticmethod
    def inputBookSearchType():
        
        while True:
            searchType = input("Please enter a search type, you can enter ISBN, Title or Author:")
            if (searchType == 'ISBN') or (searchType == 'Title') or (searchType == 'Author'):
                return searchType
            else:
                print('Invalid Search Type!')
        
        
        