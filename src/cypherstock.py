
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from bip39 import encode_bytes as gen_mnemo, decode_phrase as recover
from os import environ as env
from struct import pack
import rsa
import secrets

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, HMAC
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



# Details for the seed phrase in python comes from https://stackoverflow.com/questions/18264314/generating-a-public-private-key-pair-using-an-initial-key
# For js usage, easier package are available for 12 AND 24 words : https://crypto.stackexchange.com/questions/87314/standard-tools-for-deterministic-rsa-key-generation-using-seed
class _PRNG(object):
  def __init__(self, seed):
    self.index = 0
    self.seed = seed
    self.buffer = b""

  def __call__(self, n):
    while len(self.buffer) < n:
        self.buffer += HMAC.new(self.seed +
                                pack("<I", self.index), digestmod=SHA512).digest()
        self.index += 1
    result, self.buffer = self.buffer[:n], self.buffer[n:]
    return result


def gen_profile(pwd: str, seed: str = None, secure: bool = False) -> tuple[str, str, str]:
    if not seed:
        masterkey = RSA.generate(2048).exportKey('DER')
        raw_seed = PBKDF2(masterkey, get_random_bytes(16), 16 if not secure else 32, hmac_hash_module=SHA512)
        seed = gen_mnemo(raw_seed)
    else:
        raw_seed = recover(seed)
    privkey = RSA.generate(2048, randfunc=_PRNG(raw_seed))
    pubkey = privkey.publickey()
    pub = '-'.join(pubkey.export_key()[27:-25].decode('utf-8').split('\n'))
    priv = _pwd_encrypt('-'.join(privkey.export_key()[32:-30].decode('utf-8').split('\n')).encode('utf-8'), pwd)
    return pub, priv, seed 

def gen_token(id: str, priv: bin, pwd: str):
    privkey = rsa.PrivateKey.load_pkcs1(b'-----BEGIN RSA PRIVATE KEY-----\n' + _pwd_decrypt(priv, pwd) + b'\n-----END RSA PRIVATE KEY-----')
    val = str(int(datetime.now().timestamp() + int(env["MAX_TO"])))
    sign = rsa.sign(val.encode('utf-8'), privkey, 'MD5')
    auth = id + "-"+val+'-'+sign.hex()
    return auth


# AES privatekey password encryption

_backend = default_backend()
_iterations = 100000

def _derive_key(password: bytes, salt: bytes, iterations: int = _iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=_backend)
    return b64e(kdf.derive(password))

def _pwd_encrypt(message: bytes, password: str, iterations: int = _iterations) -> str:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return '+'.join(b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message))
        )
    ).decode('utf-8').split('='))

def _pwd_decrypt(token: str, password: str) -> bytes:
    token = '='.join(token.split('+'))
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)



def _test():
    from serve.db import instance as db
    print("Testing token generation...")
    pub, priv, seed = gen_profile("tuturu")
    token = gen_token("lou", priv, "tuturu")
    try:
        db.verify_token(token, pub)
        print("Ok.\n")
    except Exception as err:
        print("Fail - %s\n"%err)
    
    print("Testing 12 words seed recovery...")
    pub_, priv_, seed_ = gen_profile("tuturu", seed)
    token_ = gen_token("lou", priv_, "tuturu")
    try:
        db.verify_token(token, pub_)
        db.verify_token(token_, pub)
        print("Ok.\n")
    except Exception as err:
        print("Fail - %s\n"%err)


    print("Testing \"secure\" token generation...")
    pub, priv, seed = gen_profile("tuturu", secure=True)
    token = gen_token("lou", priv, "tuturu")
    try:
        db.verify_token(token, pub)
        print("Ok.\n")
    except Exception as err:
        print("Fail - %s\n"%err)
    
    print("Testing 24 words seed recovery...")
    pub_, priv_, seed_ = gen_profile("tuturu", seed)
    token_ = gen_token("lou", priv_, "tuturu")
    try:
        db.verify_token(token, pub_)
        db.verify_token(token_, pub)
        print("Ok.\n")
    except Exception as err:
        print("Fail - %s\n"%err)


from sys import argv

def __main__(*argv):
    if len(argv) < 2 or argv[1] in ["t", "test"]:
        _test()


if __name__ == "__main__":
    __main__(argv)
