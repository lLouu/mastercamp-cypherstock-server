# Load .env
from dotenv import load_dotenv
load_dotenv()
from os import environ as env

from sys import argv
from cryptography.fernet import Fernet

from serve.lib import Runner

def _gen_AES_key():
    print(Fernet.generate_key())

def _launch():
    Runner(int(env["API_PORT"]), True).launch()

def _testing():
    pass

def _help():
    pass

def __main__(*argv):
    try:
        if len(argv) < 2:
            _launch()
        elif argv[1] in ["g", "gen", "gen-aes"]:
            _gen_AES_key()
        # Features to be implemented
        elif argv[1] in ["t", "test"]:
            _testing()
        else:
            _help()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    __main__(*argv)


# file.write("Test 1 - Creation d'un profil\n")
# file.write("localhost:3443/?auth="+auth+"&command=6&public="+pub)
# file.write('\n')

# file.write("Test 1_bis - Creation d'un second profil\n")
# file.write("localhost:3443/?auth="+_auth+"&command=6&public="+_pub)
# file.write('\n')

# file.write("Test 1_ter - Creation d'un 3e profil\n")
# file.write("localhost:3443/?auth="+mauth+"&command=6&public="+mpub)
# file.write('\n')
# file.write('\n')

# file.write("Malicious_Test 1 - Test d'usurpation\n")
# file.write("localhost:3443/?auth="+mauth+"&command=6&public="+_pub)
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 2 - Stockage de la pkey\n")
# file.write("localhost:3443/?auth="+auth+"&command=6&pkey="+'+'.join(priv.split('>')))
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 3 - Accès à la pkey\n")
# file.write("localhost:3443/?auth="+auth+"&command=0")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 4 - Remove de la pkey\n")
# file.write("localhost:3443/?auth="+auth+"&command=6&pkey=remove")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 5 - Upload d'un fichier (à rajouter dans la requête le file et les header du titre, de la desc et du timestamp)\n")
# file.write("localhost:3443/?auth="+auth+"&command=8&id=lou-uol")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 6 - Accès aux contacts\n")
# file.write("localhost:3443/?auth="+auth+"&command=1")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 7 - Accès aux infos des fichiers communs\n")
# file.write("localhost:3443/?auth="+auth+"&command=2&id=uol")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 8 - Accès au fichier (add le path du fichier)\n")
# file.write("localhost:3443/?auth="+auth+"&command=3&path=")
# file.write('\n')
# file.write('\n')

# file.write("Test Malicious 8 - Accès au fichier non accésible (add le path du fichier)\n")
# file.write("localhost:3443/?auth="+mauth+"&command=3&path=")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 9 - Accès à des pseudo\n")
# file.write("localhost:3443/?auth="+auth+"&command=4&id=uol")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 10 - Accès à la clé publique\n")
# file.write("localhost:3443/?auth="+auth+"&command=5&id=uol")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 11 - Delete doc\n")
# file.write("localhost:3443/?auth="+auth+"&command=9XXXXXXXXXXXXXXXXXXX")
# file.write('\n')
# file.write('\n')
# file.write('\n')

# file.write("Test 12 - Delete profil\n")
# file.write("localhost:3443/?auth="+auth+"&command=7")
# file.write('\n')
# file.write('\n')
# file.write('\n')



