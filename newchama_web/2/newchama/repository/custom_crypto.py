
from Crypto.Cipher import AES
from Crypto import Random
import base64

def encrypt(key, message):
    # passphrase MUST be 16, 24 or 32 bytes long, how can I do that ?
    aes = AES.new(key, AES.MODE_CFB, "IV must be 16 b ")
    return base64.b64encode(aes.encrypt(message))

def decrypt(key, encrypted):
    aes = AES.new(key, AES.MODE_CFB, "IV must be 16 b ")
    return aes.decrypt(base64.b64decode(encrypted))

if __name__=="__main__":
    key = "global subscribe"
    message = "1,terryx@newchama.com"

    msg = encrypt(key, message)
    print msg
    print decrypt(key, msg)


    message = "117,terry@newchama.com,54"
    msg = encrypt(key, message)
    print msg
    print decrypt(key, msg)