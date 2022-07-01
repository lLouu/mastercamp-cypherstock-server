from datetime import datetime
from typing_extensions import Self
from mysql import connector
from os import environ as env
from rsa import PublicKey, verify
from json import loads
from serve.FA import verify as faverify

from serve.exeptions import FANotPassed, ThisGuyTriedSomethingFishy, ThisIsNotAValidTokenBoy, ExpiredToken, TokenNeedToExpireSooner

_log_db = env["LOG_FOLDER"] + "db.log"
_log_file = open(_log_db, 'a')
_log_file.write(datetime.now().isoformat() + " - Started logging database request passing throught _raiser from db.py\nThe separator is the following line\n===\n")
_log_file.close()

class _DataBase():
    def __init__(self: Self) -> None:
        self.__connector = connector.connect(
            host=env["DB_HOST"],
            database=env["DB_NAME"],
            user=env["DB_USER"],
            password=env["DB_PWD"],
            port=env["DB_PORT"]
        )
        self.reconnecting = False
        if env["CONSTANT_DB"] != "1":
            file = open(env["DB_ARCHI"])
            self.__architecture = loads(file.read())
            file.close()
            self.__verify_db()

    def verify_token(self: Self, authtoken: str, public: str = None) -> str:
        id, token, sign = authtoken.split('-')
        if not id.isalnum() or not token.isdigit():
            raise ThisGuyTriedSomethingFishy
        if int(token) < datetime.now().timestamp():
            raise ExpiredToken
        if int(token) > datetime.now().timestamp() + int(env["MAX_TO"]):
            raise TokenNeedToExpireSooner
        cursor = self.__connector.cursor(buffered=True)
        cursor.execute("SELECT public FROM user_table WHERE id=\'%s\'"%id)
        fetched_public = cursor.fetchall()
        cursor.close()
        if len(fetched_public):
            public = fetched_public[0][0]
        if not public:
            raise ThisIsNotAValidTokenBoy
            
        bin_public = b'-----BEGIN PUBLIC KEY-----\n' + '\n'.join(public.split('-')).encode('utf-8') + b'\n-----END PUBLIC KEY-----\n'
        pub = PublicKey.load_pkcs1_openssl_pem(bin_public)
        verify(token.encode('utf-8'), bytes.fromhex(sign), pub) # verify raise an error if failed
        return id

    def __tryer(self: Self, cmd: str):
        cursor = self.__connector.cursor(buffered=True)
        try:
            cursor.execute(cmd)
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def __verify_db(self: Self):
        if env["CONSTANT_DB"] == "1":
            return
        self.__reconnect()
        for table in list(self.__architecture.keys()):
            string = ""
            columns = list(self.__architecture[table].keys())
            for column in columns:
                string += ", " + column
            # Test if a table or a collumn is missing
            test = self.__tryer("SELECT " + ("*" if string == "" else string[2:]) + " FROM %s"%table)
            if not test:
                # Verify if the table exsist
                test = self.__tryer("SELECT * FROM %s"%table)
                if test:
                    previous_column = None
                    for column in columns:
                        if not self.__tryer("SELECT %s FROM %s"%(column,table)):
                            cursor = self.__connector.cursor(buffered=True)
                            cursor.execute("ALTER TABLE %s ADD %s %s"%(table, column, self.__architecture[table][column]["type"]) + (" FIRST" if not previous_column else " AFTER " + previous_column))
                            self.__connector.commit()
                            cursor.close()
                        previous_column = column
                else:
                    if len(columns):
                        string = " ("
                        primary = ""
                        for column in columns:
                            colkeys = list(self.__architecture[table][column].keys())
                            string += column + " " + self.__architecture[table][column]["type"] + ", "
                            if "primary" in colkeys:
                                primary += column + ", "
                            if "unique" in colkeys:
                                string += "UNIQUE(" + column + "), "
                            if "foreign" in colkeys:
                                string += "FOREIGN KEY(" + column + ") REFERENCES " + self.__architecture[table][column]["foreign"] + ", "
                        if primary != "":
                            string += "PRIMARY KEY(%s))"%primary[:-2]
                        else:
                            string = string[:-2] + ")"
                    else:
                        string = ""
                    cursor = self.__connector.cursor(buffered=True)
                    cursor.execute("CREATE TABLE %s%s"%(table, string))
                    self.__connector.commit()
                    cursor.close()

    def fetch(self: Self, authtoken: str, fetcher: str, public: str = None) -> list:
        cursor = self.__raiser(authtoken, fetcher, public)
        if cursor:
            data = cursor.fetchall()
            cursor.close()
            return data
        return None
    def commit(self: Self, authtoken: str, committer: str, public: str = None) -> bool:
        cursor = self.__raiser(authtoken, committer, public)
        if cursor:
            self.__connector.commit()
            cursor.close()
            return True
        return False
    def __raiser(self: Self, authtoken: str, verifyer: str, public: str = None) -> connector.cursor:
        self.__reconnect()
        self.verify_token(authtoken, public)
        cursor = self.__connector.cursor(buffered=True)
        try:
            cursor.execute(verifyer)
            _log_file = open(_log_db, 'a')
            _log_file.write(verifyer + "\n===\n")
            _log_file.close()
            return cursor
        except:
            _log_file = open(_log_db, 'a')
            _log_file.write("Data Base can't find : " + verifyer + "\n===\n")
            _log_file.close()
            cursor.close()
            return None
    
    def FA_fetch(self: Self, FA: str, id: str) -> str:
        self.__reconnect()
        cursor = self.__connector.cursor(buffered=True)
        try:
            cursor.execute("SELECT cpkey, secret FROM pkeys WHERE id = \'%s\'"%id)
            _log_file = open(_log_db, 'a')
            _log_file.write("SELECT cpkey, secret FROM pkeys WHERE id = \'%s\'\n===\n"%id)
            _log_file.close()
        except:
            _log_file = open(_log_db, 'a')
            _log_file.write("Data Base can't find : SELECT cpkey, secret FROM pkeys WHERE id = \'%s\' \n===\n"%id)
            _log_file.close()
            cursor.close()
            return None
        pkey, secret = cursor.fetchall()[0]
        cursor.close()
        if not faverify(secret, FA):
            raise FANotPassed
        return pkey
        



    def __reconnect(self):
        if self.reconnecting:
            while self.reconnecting:
                pass
            return
        self.reconnecting = True
        while not self.__connector.is_connected():
            try:
                self.__connector.ping(reconnect=True, attempts=120, delay=5)
            except:
                _log_file = open(_log_db, 'a')
                _log_file.write("The connexion to the data base doesn't revive (" + datetime.utcnow().isoformat() +")\n===\n") ## Review expetions handling
                _log_file.close()
        self.reconnecting = False

instance = _DataBase()