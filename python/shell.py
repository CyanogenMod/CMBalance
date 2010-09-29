from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn
from subprocess import Popen
import os.path

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """ threaded server """

class Server(object):
    def __init__(self):
        root = "/home/ctso/cm"

        self.paths = {
            'root': root,
            'nightly': os.path.join(root, 'nightly'),
            'stable': os.path.join(root, 'stable'),
        }

    def ping(self):
        return "pong"

    def sync(self):
        o = Popen('rsync -avh rsync://cyanogenmod.com/nightly ' + self.paths['nightly'], shell=True)
        print o
        return True

    def fileExists(self, type, path):
        path = os.path.join(self.paths[type], path)

        if os.path.exists(path):
            return True
        else:
            return False

def main():
    server = ThreadedXMLRPCServer(("localhost", 49150))
    server.register_instance(Server())
    server.serve_forever()

if __name__ == '__main__':
    main()
