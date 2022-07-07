# Load .env
from dotenv import load_dotenv
load_dotenv()
from os import environ as env

from sys import argv

def _gen_AES_key():
    from cryptography.fernet import Fernet
    print(Fernet.generate_key())

def _launch(port: int = int(env["API_PORT"])):
    from serve.lib import Runner
    Runner(port, True).launch()

def _sample(adr: str):
    from requests import post
    from cypherstock import gen_profile, gen_token
    from cryptography.fernet import Fernet
    from rsa import PublicKey, encrypt

    print("Generating accounts...")
    print("0/5")
    adr = "http://" + adr + "/?auth=%s&command="
    pubA, priv, seed = gen_profile("password")
    tokenA = gen_token("MonsieurA", priv, "password")
    r = post(adr%tokenA + "6&public=" + pubA).content
    if r != b"success":
        print("The samples seems to already be setted")
        return
    print("1/5")
    admin_pub = post(adr%tokenA + "5&id=admin").content
    if admin_pub == b'NULL':
        print("Please create an admin user before asking for samples")
        return
    else:
        pem = b'-----BEGIN PUBLIC KEY-----\n' + ('\n'.join(admin_pub.decode('utf-8').split('\n')[0].split('-'))).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n'
        admin_pub = PublicKey.load_pkcs1_openssl_pem(pem) 
    pubB, priv, seed = gen_profile("password")
    tokenB = gen_token("MonsieurB", priv, "password")
    post(adr%tokenB + "6&public=" + pubB).content
    print("2/5")
    pubC, priv, seed = gen_profile("password")
    tokenC = gen_token("MonsieurC", priv, "password")
    post(adr%tokenC + "6&public=" + pubC).content
    print("3/5")
    pubD, priv, seed = gen_profile("password")
    tokenD = gen_token("MonsieurD", priv, "password")
    post(adr%tokenD + "6&public=" + pubD).content
    print("4/5")
    pubE, priv, seed = gen_profile("password")
    tokenE = gen_token("MonsieurE", priv, "password")
    post(adr%tokenE + "6&public=" + pubE).content
    print("5/5")


    print("getting public keys")
    pubA = PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pubA.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n')
    pubB = PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pubB.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n')
    pubC = PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pubC.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n')
    pubD = PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pubD.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n')
    pubE = PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(pubE.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n')
    print("Done")


    print("Generating files")
    print("0/10")
    key = Fernet.generate_key()
    file1 = Fernet(key).encrypt(b"Bonjour file")
    post(adr%tokenA + "8&id=admin-MonsieurA&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubA).hex(), data=file1, headers={"XEU-name" : "Bonjour", "XEU-desc" : "Description de bonjour"}).content
    print("1/10")
    key = Fernet.generate_key()
    file2 = Fernet(key).encrypt(b"Salut file")
    post(adr%tokenA + "8&id=admin-MonsieurA-MonsieurB&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubA).hex() + "-" + encrypt(key, pubB).hex(), data=file2, headers={"XEU-name" : "Salut", "XEU-desc" : "Description de salut"}).content
    print("2/10")
    key = Fernet.generate_key()
    file3 = Fernet(key).encrypt(b"Hola file")
    post(adr%tokenB + "8&id=admin-MonsieurB&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubB).hex(), data=file3, headers={"XEU-name" : "Hola", "XEU-desc" : "Description de Hola"}).content
    print("3/10")
    key = Fernet.generate_key()
    file4 = Fernet(key).encrypt(b"Ohayo file")
    post(adr%tokenB + "8&id=admin-MonsieurB-MonsieurE&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubB).hex() + "-" + encrypt(key, pubE).hex(), data=file4, headers={"XEU-name" : "Ohayo", "XEU-desc" : "Description de Ohayo"}).content
    print("4/10")
    key = Fernet.generate_key()
    file5 = Fernet(key).encrypt(b"Dez mat file")
    post(adr%tokenB + "8&id=admin-MonsieurB&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubB).hex(), data=file5, headers={"XEU-name" : "Dez mat", "XEU-desc" : "Description de Dez mat"}).content
    print("5/10")
    key = Fernet.generate_key()
    file6 = Fernet(key).encrypt(b"Hello file")
    post(adr%tokenC + "8&id=admin-MonsieurC&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubC).hex(), data=file6, headers={"XEU-name" : "Hello", "XEU-desc" : "Description de Hello"}).content
    print("6/10")
    key = Fernet.generate_key()
    file7 = Fernet(key).encrypt(b"Hy file")
    post(adr%tokenD + "8&id=admin-MonsieurD-MonsieurE&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubD).hex() + "-" + encrypt(key, pubE).hex(), data=file7, headers={"XEU-name" : "Hy", "XEU-desc" : "Description de Hy"}).content
    print("7/10")
    key = Fernet.generate_key()
    file8 = Fernet(key).encrypt(b"Tuturu file")
    post(adr%tokenD + "8&id=admin-MonsieurD&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubD).hex(), data=file8, headers={"XEU-name" : "Tuturu", "XEU-desc" : "Description de Tuturu"}).content
    print("8/10")
    key = Fernet.generate_key()
    file9 = Fernet(key).encrypt(b"Bonsoir file")
    post(adr%tokenD + "8&id=admin-MonsieurD&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubD).hex(), data=file9, headers={"XEU-name" : "Bonsoir", "XEU-desc" : "Description de Bonsoir"}).content
    print("9/10")
    key = Fernet.generate_key()
    file10 = Fernet(key).encrypt(b"Hallo file")
    post(adr%tokenD + "8&id=admin-MonsieurD-MonsieurE-MonsieurA&sym=" + encrypt(key, admin_pub).hex() + "-" + encrypt(key, pubD).hex() + "-" + encrypt(key, pubE).hex(), data=file10, headers={"XEU-name" : "Hallo", "XEU-desc" : "Description de Hallo"}).content
    print("10/10")
            

def _testing(adr: str):
    from requests import post
    from cypherstock import gen_profile, gen_token
    try:
        print("Testing Profile creation...")
        pub, priv, seed = gen_profile("tuturu")
        token = gen_token("lou", priv, "tuturu")
        adr = "http://" + adr + "/?auth=%s&command="
        r = post(adr%token + "6&public=" + pub).content
        if r != b"success":
            print("Bad request")
            raise Exception
        print("Ok...\n")

        print("Testing pseudo access...")
        r = post(adr%token + "4&id=lou").content
        if r != b"lou":
            print("Bad request")
            raise Exception
        print("Ok...\n")

        print("Testing public key access...")
        r = post(adr%token + "5&id=lou").content
        if r.decode('utf-8').split('\n')[0] != pub:
            print("Bad request")
            raise Exception
        print("Ok...\n")

        print("Testing enabling 2FA...")
        from serve.FA import gen_secret, get_totp_token
        secret = gen_secret()
        r = post(adr%token + "6&pkey=%s&secret=%s"%(priv, secret)).content
        if r != b"success":
            print("Bad request")
            raise Exception
        print("Ok...\n")

        print("Testing access to pkey with 2FA...")
        r = post((adr%'')[:-14] + "command=0&id=lou&fa=" + get_totp_token(secret)).content
        if r.decode('utf-8') != priv:
            print("Bad request")
            raise Exception
        print("Ok...\n")

        print("Testing disabling 2FA...")
        r = post(adr%token + "6&pkey=remove&fa=%s"%(get_totp_token(secret))).content
        if r != b"success":
            print("Bad request")
            raise Exception
        print("Ok...\n")

        try:
            file = {}
            print("Creation of two other profiles...")
            pub, priv, seed = gen_profile("tuturu")
            token_ = gen_token("oul", priv, "tuturu")
            r = post(adr%token_ + "6&public=" + pub).content
            if r != b"success":
                print("Bad request")
                raise Exception
            pub, priv, seed = gen_profile("tuturu")
            token__ = gen_token("ulo", priv, "tuturu")
            r = post(adr%token__ + "6&public=" + pub).content
            if r != b"success":
                print("Bad request")
                raise Exception
            print("Ok...\n")

            print("Upload of three random file for all three profiles...")
            from secrets import token_bytes
            file1 = token_bytes(16384)
            r = post(adr%token + "8&id=lou-oul-ulo", data=file1, headers={"XEU-name" : "okarin", "XEU-desc" : "This should be seen by everyone"}).content
            if r != b"success":
                print("Bad request")
                raise Exception
            file2 = token_bytes(16384)
            r = post(adr%token + "8&id=lou-oul", data=file2, headers={"XEU-name" : "okarin", "XEU-desc" : "This should be seen by lou and oul"}).content
            if r != b"success":
                print("Bad request")
                raise Exception
            file3 = token_bytes(16384)
            r = post(adr%token + "8&id=lou-ulo", data=file3, headers={"XEU-name" : "okarin", "XEU-desc" : "This should be seen by lou and ulo"}).content
            if r != b"success":
                print("Bad request")
                raise Exception
            print("Ok...\n")

            print("Get contacts...")
            r = post(adr%token + "1").content
            if r != b"[('lou',), ('oul',), ('ulo',)]":
                print("Bad request")
                raise Exception
            print("Ok...\n")

            print("Verify files access...")
            r = post(adr%token + "2&id=oul").content.decode('utf-8').split('\n\n')
            if r[0].split('-')[-1] != "This should be seen by everyone" or r[1].split('-')[-1] != "This should be seen by lou and oul":
                print("Bad request")
                raise Exception
            file = {"1": '-'.join(r[0].split('-')[:-1]), "2": '-'.join(r[1].split('-')[:-1])}
            r = post(adr%token + "2&id=ulo").content.decode('utf-8').split('\n\n')
            if r[0].split('-')[-1] != "This should be seen by everyone" or r[1].split('-')[-1] != "This should be seen by lou and ulo":
                print("Bad request")
                raise Exception
            file["3"] = '-'.join(r[1].split('-')[:-1])
            print("Ok...\n")

            print("Verify file data...")
            r = post(adr%token + "3&path=%s"%file["1"]).content
            if r[1:] != file1:
                print("Bad request")
                raise Exception
            r = post(adr%token + "3&path=%s"%file["2"]).content
            if r[1:] != file2:
                print("Bad request")
                raise Exception
            r = post(adr%token + "3&path=%s"%file["3"]).content
            if r[1:] != file3:
                print("Bad request")
                raise Exception
            print("Ok...\n")
        except Exception as err:
            print("Failed - %s\nStopping tests...\n"%err)
        
        print("Deleting files...")
        for key in list(file.keys()):
            r = post(adr%token + "9&path=%s"%file[key]).content
            if r != b"success":
                print("Bad request")
        print("Ok...\n")

        print("Deleting secondary profiles...")
        r = post(adr%token_ + "7").content
        if r != b"success":
            print("Bad request")
        r = post(adr%token__ + "7").content
        if r != b"success":
            print("Bad request")
        print("Ok...\n")
    except Exception as err:
        print("Failed - %s\nStopping tests...\n"%err)

    print("Testing profile deletion...")
    r = post(adr%token + "7").content
    if r != b"success":
        print("Bad request")
    print("Ok...\n")

def _help():
    print("\n\n\n\nCypherStock API CLI -\nBy XEU\n\napi.py [port]\t\t- Launch the api on the port putted. Default value is setted in .env\napi.py g|gen|gen-aes\t- Give a random AES key for SLE_KEY\napi.py t|test <ip>\t- execute the test script on the ip\n\n")

def __main__(*argv):
    try:
        if len(argv) < 2:
            _launch()
        elif argv[1].isdigit():
            _launch(argv[1])
        elif argv[1] in ["g", "gen", "gen-aes"]:
            _gen_AES_key()
        elif argv[1] in ["t", "test"] and len(argv) >= 3:
            _testing(argv[2])
        elif argv[1] in ["s", "sample"]:
            _sample(argv[2]);
        else:
            _help()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    __main__(*argv)

