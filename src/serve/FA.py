# mainly from https://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
# Need to be review & secured

from base64 import b32decode
from struct import pack, unpack
import hmac
from hashlib import sha1
from time import time
from secrets import choice

def _get_hotp_token(secret, intervals_no):
    key = b32decode(secret, True)
    msg = pack(">Q", intervals_no)
    h = hmac.new(key, msg, sha1).digest()
    o = h[19] & 15
    h = (unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return str(h)

def get_totp_token(secret):
    return _get_hotp_token(secret, intervals_no=int(time())//30)

def _get_timed_totp_token(secret):
    return _get_hotp_token(secret, intervals_no=int(time()-0.5)//30)

def verify(secret, auth):
    return auth == _get_timed_totp_token(secret)

def gen_secret():
    t = ''
    for _ in range(16):
        t += choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
    return t