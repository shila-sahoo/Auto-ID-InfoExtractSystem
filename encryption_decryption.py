from base64 import b64decode
from base64 import  b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad

import base64
from codecs import encode


class data_security:
    def __init__(self):
        self.encryption_key = "PasswordPasswordPasswordPassword"

    def encrypt(self, path):
        with open(path, 'rb') as f:
            plain = f.read()
            bin_img = base64.b64encode(plain).decode()
        ivs = b'dynamic@dynamic@'
        text=bin_img.encode('utf-8')
        my_cipher = AES.new(key=self.encryption_key.encode('utf-8'),mode=AES.MODE_CBC,iv=ivs)
        result=b64encode(my_cipher.encrypt(pad(text,AES.block_size))).decode('utf-8')
        '''with open(save_path, 'w') as f:
            f.write(result)'''
        return result

    def decrypt(self, encr_str, save_path):
        '''with open(path, 'r') as f:
            encr = f.read()'''
        ivs = b'dynamic@dynamic@'
        my_cipher = AES.new(
            key=self.encryption_key.encode('utf-8'),
            mode=AES.MODE_CBC,
            iv=ivs
        )
        result = unpad(my_cipher.decrypt(b64decode(encr_str)),AES.block_size).decode('utf-8')
        binary_img = base64.b64decode(result)
        with open(save_path, "wb") as f:
            f.write(binary_img)
