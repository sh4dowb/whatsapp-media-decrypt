#!/usr/bin/python3

from Crypto.Cipher import AES
import hashlib
import hmac
import base64
import sys


appInfo = {
    "image": b"WhatsApp Image Keys",
    "video": b"WhatsApp Video Keys",
    "audio": b"WhatsApp Audio Keys",
    "document": b"WhatsApp Document Keys",
    "image/webp": b"WhatsApp Image Keys",
    "image/jpeg": b"WhatsApp Image Keys",
    "image/png": b"WhatsApp Image Keys",
    "video/mp4": b"WhatsApp Video Keys",
    "audio/aac": b"WhatsApp Audio Keys",
    "audio/ogg": b"WhatsApp Audio Keys",
    "audio/wav": b"WhatsApp Audio Keys",
}

extension = {
    "image": "jpg",
    "video": "mp4",
    "audio": "ogg",
    "document": "bin",
}


def HKDF(key, length, appInfo=b""):
    key = hmac.new(b"\0"*32, key, hashlib.sha256).digest()
    keyStream = b""
    keyBlock = b""
    blockIndex = 1
    while len(keyStream) < length:
        keyBlock = hmac.new(
            key,
            msg=keyBlock+appInfo + (chr(blockIndex).encode("utf-8")),
            digestmod=hashlib.sha256).digest()
        blockIndex += 1
        keyStream += keyBlock
    return keyStream[:length]


def AESUnpad(s):
    return s[:-ord(s[len(s)-1:])]


def AESDecrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return AESUnpad(plaintext)


def decrypt(fileName, mediaKey, mediaType, output):
    mediaKeyExpanded = HKDF(mediaKey, 112, appInfo[mediaType])
    macKey = mediaKeyExpanded[48:80]
    mediaData = open(fileName, "rb").read()

    file = mediaData[:-10]
    mac = mediaData[-10:]

    data = AESDecrypt(mediaKeyExpanded[16:48], file, mediaKeyExpanded[:16])

    if output is None:
        if "/" in mediaType:
            fileExtension = mediaType.split("/")[1]
        else:
            fileExtension = extension[mediaType]

        output = fileName.replace('.enc', '.{}'.format(fileExtension))
    with open(output, 'wb') as f:
        f.write(data)

    return True


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(version='1')
    parser.add_option(
        '-m',
        '--mime',
        dest='mediaType',
        default='image',
        help="media type of the encrypted file. Default 'image'"
    )
    parser.add_option(
        '-b',
        '--base64',
        dest='base64Key',
        default=None,
        help='media key in Base64'
    )
    parser.add_option(
        '-j',
        '--hex',
        dest='hexKey',
        default=None,
        help='media key in Hex'
    )
    parser.add_option(
        '-o',
        '--output',
        dest='output',
        default=None,
        help='path for the plaintext'
    )
    (options, args) = parser.parse_args()

    fileName = args[0]
    if options.base64Key is not None:
        mediaKey = base64.b64decode(options.base64Key)
    elif options.hexKey is not None:
        mediaKey = bytes.fromhex(options.hexKey)
    else:
        print("You must specify the key in either "
              "Base64 or Hex.\nUsage: decrypt.py -h")
        sys.exit(1)

    if decrypt(fileName, mediaKey, options.mediaType, options.output):
        print("Decrypted (hopefully)")
