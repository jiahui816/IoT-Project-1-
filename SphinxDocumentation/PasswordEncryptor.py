class PasswordEncryptor:
    'This class for password encryption'
    @staticmethod
    def hashPassword(password):
        '''
        This function is to generate an hash value for the accout password.
           Args:
            param1:Account password
        '''
        hashedPassword = sha256_crypt.hash(password)
        
        return hashedPassword
    
    @staticmethod
    def verifyPassword(password, hashedPassword):
        '''
        This function is to compare the current entered password to the hashedPasword.
           Args:
            param1:Current Object
            param2:Hashed password

           Returns:
            Boolean value
        '''
        if(sha256_crypt.verify(password, hashedPassword)):
            return True

        return False