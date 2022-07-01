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
        # Features to be implemented
        elif argv[1] in ["t", "test"] and len(argv) >= 3:
            _testing(argv[2])
        else:
            _help()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    __main__(*argv)

