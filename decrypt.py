from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib
import hmac
import base64
import sys

fileName = sys.argv[1]
mediaKey = sys.argv[2]

def HKDF(key, length, appInfo=b""):
    key = hmac.new(b"\0"*32, key, hashlib.sha256).digest()
    keyStream = b""
    keyBlock = b""
    blockIndex = 1
    while len(keyStream) < length:
        keyBlock = hmac.new(key, msg=keyBlock+appInfo+(chr(blockIndex).encode("utf-8")), digestmod=hashlib.sha256).digest()
        blockIndex += 1
        keyStream += keyBlock
    return keyStream[:length]

def AESUnpad(s):
    return s[:-ord(s[len(s)-1:])];

def AESDecrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv);
    plaintext = cipher.decrypt(ciphertext);
    return AESUnpad(plaintext);

mediaKeyExpanded=HKDF(base64.b64decode(mediaKey),112,b"WhatsApp Image Keys")
macKey=mediaKeyExpanded[48:80]
mediaData=open(fileName,"rb").read()

file= mediaData[:-10]
mac= mediaData[-10:]

imgdata=AESDecrypt(mediaKeyExpanded[16:48],file, mediaKeyExpanded[:16])

with open(fileName.replace('.enc', '.bin'), 'wb') as f:
    f.write(imgdata)

print("Decrypted image (hopefully)")
