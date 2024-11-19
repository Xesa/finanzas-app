import base64
from nacl.public import PrivateKey, Box
from config import Constants

def validateToken(token):
    # Checks the facilitated token against the validation token stored in the Secrets file

    try:
        validationToken = Constants.get('VALIDATION_TOKEN', "s")

        if (validationToken is None):
            raise Exception('Validation Token is missing.')

        if (token == "" or token != validationToken):
            return False
        else:
            return True

    except Exception as err:
        print(err)
        return err

def setSecretToken():
    # Sets a new secret token to encrypt the credentials

    privateKey = PrivateKey.generate()
    privateKey64 = base64.b64encode(privateKey.encode()).decode('utf-8')
    Constants.write("SECRET_TOKEN", privateKey64, "s")
    return privateKey64

def getSecretToken():
    # Gets the secret token stored in the Secrets file

    secretToken = Constants.get('SECRET_TOKEN', "s")

    if (secretToken is None):
        return setSecretToken()
    else:
        return secretToken

def getCipher(secretToken):
    # Gets a cipher that can encrypt and decrypt the credentials

    privateKey = PrivateKey(base64.b64decode(secretToken))
    publicKey = privateKey.public_key
    return Box(privateKey, publicKey)