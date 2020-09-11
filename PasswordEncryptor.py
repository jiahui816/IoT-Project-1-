from passlib.hash import sha256_crypt

class PasswordEncryptor:

    @staticmethod
    def hashPassword(password):

        hashedPassword = sha256_crypt.hash(password)
        
        return hashedPassword
    
    @staticmethod
    def verifyPassword(password, hashedPassword):

        if(sha256_crypt.verify(password, hashedPassword)):
            return True

        return False