# whatsapp-media-decrypt
Decrypt WhatsApp .enc media files with Python

Usage:

With Base64 key
```shell
$ python3 decrypt.py -b "iT8tVH4pip+GYbL58iAk01x3Ih7Ks7l7+gfS90SfQzQ=" file.enc
Decrypted (hopefully)
```
or with Hex key
```shell
$ python3 decrypt.py -j "893f2d547e298a9f8661b2f9f22024d35c77221ecab3b97bfa07d2f7449f4334" file.enc
Decrypted (hopefully)
```
```shell
$ file file.bin
file.bin: PNG image data, 540 x 720, 8-bit/color RGB, non-interlaced
```
