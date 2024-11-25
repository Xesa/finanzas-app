import base64
import nacl.utils
from nacl.public import PrivateKey, Box
from config import Constants

class Cipher:
    _cipher = None

    @classmethod
    def _instantiateCipher(cls):
        # Checks if the cipher is already instantiated
        if (cls._cipher is not None):
            return cls._cipher

        # Creates a cipher that can encrypt and decrypt the credentials
        privateKey = cls._getSecretToken()
        cls._cipher = Box(privateKey, privateKey.public_key)

        return cls._cipher

    @classmethod
    def _setSecretToken(cls):
        # Sets a new secret token to encrypt the credentials
        privateKey = PrivateKey.generate()

        # Writes it in the secrets file as a base64
        privateKey64 = base64.b64encode(privateKey.encode()).decode('utf-8')
        Constants.write("SECRET_TOKEN", privateKey64, "s")

        return privateKey

    @classmethod
    def _getSecretToken(cls):
        # Gets the secret token stored in the Secrets file
        secretToken = Constants.get('SECRET_TOKEN', "s")

        # If it's valid returns it, if not, sets a new one
        if (secretToken is not None):
            return PrivateKey(base64.b64decode(secretToken))
        else:
            return cls._setSecretToken()

    @classmethod
    def encryptElement(cls, element):
        cipher = cls._instantiateCipher()

        # Encrypts the element
        bytes = element.encode('utf-8')
        nonce = nacl.utils.random(nacl.public.Box.NONCE_SIZE)
        encryptedElement = cipher.encrypt(bytes, nonce)

        # Converts the nonce and the encrypted element into a base64 string
        base64nonce = base64.b64encode(nonce).decode('utf-8')
        base64encrypted = base64.b64encode(encryptedElement.ciphertext).decode('utf-8')

        # Joins the strings as a unique encrypted element
        return base64nonce + base64encrypted

    @classmethod
    def decryptElement(cls, element):
        cipher = cls._instantiateCipher()

        # Decodes the base64 strings
        nonce = base64.b64decode(element)[:nacl.public.Box.NONCE_SIZE]
        encryptedElement = base64.b64decode(element)[nacl.public.Box.NONCE_SIZE:]

        # Decrypts the element
        return cipher.decrypt(encryptedElement, nonce).decode('utf-8')