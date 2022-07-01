from http.server import CGIHTTPRequestHandler
from json import loads
from socketserver import ThreadingTCPServer, BaseRequestHandler, BaseServer
from ssl import wrap_socket
from threading import Thread
from typing import Any, Callable
from typing_extensions import Self
from os import environ as env, remove
from os.path import exists
import gzip
from datetime import datetime
from cryptography.fernet import Fernet


from serve.db import instance as db
from serve.exeptions import NoAuthTokenGiven, NothingAsked, FANeeded, FANotPassed, ThisGuyTriedSomethingFishy, NotEnoughtDataForRequest, AccessRefused
from serve.FA import verify

_log_string = env["LOG_FOLDER"] + 'verif-string.log'
_log_file = open(_log_string, 'a')
_log_file.write(datetime.now().isoformat() + " - Started logging negative string passing _verify_string function -lib.py-\nThe separator is the following line\n==_==-----==_==-----==_==\n")
_log_file.close()

# verify s considering the whitelist '-', '+', '/', '_' and alphanum characters. 
def _verify_string(s : str) -> bool:
    s = ''.join(s.split('-'))
    s = ''.join(s.split('+'))
    s = ''.join(s.split('/'))
    s = ''.join(s.split('_'))
    ret = s.isalnum()
    if not ret:
        _log_file = open(_log_string, 'a')
        _log_file.write(s + '\n==_==-----==_==-----==_==\n')
        _log_file.close()
    return ret

# Custom class of Threading TCPServer from socketserver
class _Server(ThreadingTCPServer):
    def __init__(self: Self, server_address: tuple[str, int], RequestHandlerClass: Callable[[Any, Any, Self], BaseRequestHandler], bind_and_activate: bool = True) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        # Activate https if setted up
        if env["SSL_ON"] == "1":
            self.socket = wrap_socket(self.socket,
                                keyfile=env["SSL_KEY_PATH"],
                                certfile=env["SSL_CERT_PATH"],
                                server_side=True)

    # def verify_request(self: Self, request: bytes, client_address: tuple[str, int]) -> bool:
    #     ## Custom Anti-DDoS & request verif & Black list here
    #     return True

# Base Handler class
class _Handler(CGIHTTPRequestHandler):
    def __init__(self: Self, request: bytes, client_address: tuple[str, int], server: BaseServer, directory: str = None) -> None:
        # Make the default error template modulable
        file = open(env["ERROR_TEMPLATE"], "r")
        self.error_message_format = file.read()
        super().__init__(request, client_address, server)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.set_header()
    
    def set_header(self: Self):
        self.send_header("Content-type", "text/plain;charset=utf-8")
        self.end_headers()

# Handler for web app requests
class _HTTPSHandler(_Handler):
    def __init__(self: Self, request: bytes, client_address: tuple[str, int], server: _Server, directory: str =None) -> None:
        super().__init__(request, client_address, server)

    def set_header(self: Self) -> str:
        self.accessible = open(env["HTTP_PATH"] + "accessible.dat", "r").read().split('\n')
        self.answered = loads(open(env["HTTP_PATH"] + "answered.dat", "r").read())
        link = self.path if not '?' in self.path else self.path.split('?')[0]
        if link in self.accessible: ## Review path
            self.send_response(200)
            ext = link.split('/')[-2]
            ## Review header
            self.send_header("Content-type", "text/" + ext + ";charset=utf-8")
            self.send_header("Cache-Control", "public,max-age=" + env["CACHER_TO"] + ",must-revalidate")
            path = env["HTTP_PATH"] + link[1:]
        elif link in list(self.answered.keys()):
            ## Review header
            self.send_response(200)
            self.send_header("Content-type", "text/html;charset=utf-8")
            path = env["HTTP_PATH"] + self.answered[link]
        else:
            self.send_error(404)
        self.end_headers()
        return path

    def do_GET(self: Self) -> None:
        try:
            path = self.set_header()
            file = open(path, "r")
            self.wfile.write(file.read().encode("utf-8"))
        except:
            self.send_error(404)

    def do_POST(self: Self) -> None:
        self.send_error(405)
        

class _APIHandler(_Handler):
    def __init__(self: Self, request: bytes, client_address: tuple[str, int], server: _Server, directory: str =None) -> None:
        super().__init__(request, client_address, server)

    def set_header(self: Self):
        ## Review header
        self.send_response(200)
        self.send_header("Content-type", "text/plain;charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self: Self) -> None:
        self.send_error(405)

    def do_POST(self: Self) -> None:
        try:
            raw_param = [] if not '?' in self.path else self.path.split('?')[-1].split('&')
            data = {}
            for d in raw_param:
                index, value = d.split('=', 2)
                if not _verify_string(index) or not _verify_string(value):
                    raise ThisGuyTriedSomethingFishy
                data[index] = value
            keys = list(data.keys())

            if not "auth" in keys:
                raise NoAuthTokenGiven
            if not "command" in keys:
                raise NothingAsked
            
            body = 'NULL'.encode('utf-8')
            id = data["auth"].split('-')[0]

            if data["command"] == "0":
                if not "fa" in keys:
                    raise FANeeded
                c_pkey = db.FA_fetch(data["fa"], id)
                body = c_pkey.encode('utf-8')
            elif data["command"] == "1":
                ids = db.fetch(data["auth"], "SELECT DISTINCT s1.id FROM share as s1 cross join share as s2 WHERE s1.path = s2.path and s2.id = \'%s\'"%id)
                body = str(ids).encode('utf-8')
            elif data["command"] == "2":
                if not "id" in keys:
                    raise NotEnoughtDataForRequest
                paths = db.fetch(data["auth"], "SELECT s1.path from share as s1 cross join share as s2 WHERE s1.path = s2.path and s2.id = \'%s\' and s1.id = \'%s\'"%(data["id"], id))
                body = b''
                for path in paths:
                    try:
                        file = open(env["UPLOAD_PATH"] + path[0], "rb")
                        desc = file.readline()
                        file.close()
                    except:
                        desc = "/!\ compromised".encode('utf-8')
                    body += path[0].encode('utf-8') + b'-' + desc + b'\n'
            elif data["command"] == "3":
                if not "path" in keys:
                    raise NotEnoughtDataForRequest
                sym = db.fetch(data["auth"], "SELECT path, symkey FROM share WHERE path = \'%s\' and id = \'%s\'"%(data["path"], id))
                if not len(sym):
                    raise AccessRefused
                body = b''
                if sym[0][1]:
                    body += sym[0][1]
                body += '\n'.encode('utf-8')
                if exists(env["UPLOAD_PATH"] + data["path"]):
                    file = open(env["UPLOAD_PATH"] + data["path"], "rb")
                    file.readline()
                    uncomp = gzip.decompress(file.read())
                    if env["SECOND_LAYER_ENCRYPTION"] == "1":
                        uncomp = Fernet(env["SLE_KEY"]).decrypt(uncomp)
                    body += uncomp
                else:
                    body += b"/!\ Compromised"
            elif data["command"] == "4":
                if not "id" in keys:
                    raise NotEnoughtDataForRequest
                f = db.fetch(data["auth"], "SELECT id, pseudo FROM user_table")
                for duo in f:
                    if duo[0] == data["id"]:
                        body = duo[1].encode('utf-8')
                        break
            elif data["command"] == "5":
                if not "id" in keys:
                    raise NotEnoughtDataForRequest
                f = db.fetch(data["auth"], "SELECT id, public, seed FROM user_table")
                for trio in f:
                    if trio[0] == data["id"]:
                        body = (trio[1] + '\n' + trio[2]).encode('utf-8')
            elif data["command"] == "6":
                replicata = db.fetch(data["auth"], "SELECT public FROM user_table WHERE id=\'%s\'"%id, public=None if not "public" in keys else data["public"])
                if len(replicata) and "public" in keys and data["public"] != replicata[0][0]:
                    raise ThisGuyTriedSomethingFishy
                if len(replicata) and not "public" in keys:
                    data["public"] = replicata[0][0]
                if not "pkey" in keys:
                    db.commit(data["auth"], "DELETE FROM user_table WHERE id=\'%s\'"%(id), public=data["public"])
                    db.commit(data["auth"], "INSERT INTO user_table VALUES (\'%s\', \'%s\', \'%s\', \'%s\')"%(id, data["public"], "" if not "seed" in keys else data["seed"], id if not "pseudo" in keys else data["pseudo"]), public=data["public"])
                else:
                    secret = db.fetch(data["auth"], "SELECT secret FROM pkeys WHERE id=\'%s\'"%id)
                    if secret and secret[0][0]:
                        if not "fa" in keys:
                            raise FANeeded
                        if not verify(secret[0][0], data["fa"]):
                            raise FANotPassed
                    db.commit(data["auth"], "DELETE FROM pkeys WHERE id=\'%s\'"%id)
                    if data["pkey"] != "remove":
                        if not "secret" in keys:
                            raise NotEnoughtDataForRequest
                        db.commit(data["auth"], "INSERT INTO pkeys VALUES (\'%s\', \'%s\', %s)"%(id, data["pkey"], '\''+ data["secret"] +'\''))
                body = "success".encode('utf-8')
            elif data["command"] == "7":
                db.commit(data["auth"], "DELETE FROM share WHERE id=\'%s\'"%(id))
                db.commit(data["auth"], "DELETE FROM pkeys WHERE id=\'%s\'"%(id))
                db.commit(data["auth"], "DELETE FROM user_table WHERE id=\'%s\'"%(id))
                body = "success".encode('utf-8')
            elif data["command"] == "8":
                h = list(self.headers.keys())
                if not "Content-Length" in h or not "XEU-name" in h or not "id" in keys:
                    raise NotEnoughtDataForRequest
                if not self.headers["XEU-name"].isalnum() or ("XEU-to" in h and not self.headers["XEU-to"].isdigit()):
                    raise ThisGuyTriedSomethingFishy
                ids = data["id"].split('-')
                sym = [] if not "sym" in keys else data["sym"].split('-')
                name = '%s-%s-%s'%(self.headers["XEU-name"], str(int(datetime.now().timestamp())), (str(int(datetime.now().timestamp()) + int(env["UPLOAD_TO"])) if not "XEU-to" in h else self.headers["XEU-to"]))
                cmd = "INSERT INTO share VALUES "
                sub = "(\'%s\',\'" + name + ("\', NULL)" if not "sym" in keys else ",\'%s\')")
                for i in range(len(ids)):
                    if len(sym):
                        arg = (ids[i], sym[i])
                    else:
                        arg = (ids[i])
                    cmd += sub%arg + ','
                db.commit(data["auth"], cmd[:-1])
                raw_datas = self.rfile.read(int(self.headers["Content-Length"]))
                if env["SECOND_LAYER_ENCRYPTION"] == "1":
                    raw_datas = Fernet(env["SLE_KEY"]).encrypt(raw_datas)
                compressed = gzip.compress(raw_datas)
                file = open(env["UPLOAD_PATH"] + name, "wb")
                head = (("\n" if not "XEU-desc" in h else self.headers["XEU-desc"]) + "\n").encode('utf-8')
                file.write(head + compressed)
                file.close()
                body = "success".encode('utf-8')
            elif data["command"] == "9":
                if not "path" in keys:
                    raise NotEnoughtDataForRequest
                db.commit(data["auth"], "DELETE FROM share WHERE path=%s"%data["path"])
                root = env["UPLOAD_PATH"] + data["path"]
                if exists(root):
                    remove(root)
                body = "success".encode('utf-8')
            self.set_header()
            self.wfile.write(body)
        except Exception as err:
            ## Error handling
            self.send_error(400)



class Runner(Thread):
    def __init__(self: Self, port :int, is_api : bool = False) -> None:
        self._httpd = _Server(("", port), _APIHandler if is_api else _HTTPSHandler)
        super().__init__(target=self._httpd.serve_forever) ## Threading à revoir

    def launch(self):
        self.run()
        return self
