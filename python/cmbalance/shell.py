from cmbalance.settings import Settings
from cmbalance.utils import ThreadedXMLRPCServer
from subprocess import Popen
import os.path
import sys

SETTINGS_FILES = ["~/.cmbalanceconf"]

def getConfig():
    for fn in SETTINGS_FILES:
        fn = os.path.expanduser(fn)
        if os.path.exists(fn):
            return fn

class Server(object):
    def __init__(self, settings):
        self.settings = settings
        root = settings.paths.root

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
        o2 = Popen('rsync -avh rsync://chemlab.org/android ' + self.paths['stable'], shell=True)
        print o2
        return True

    def fileExists(self, type, path):
        path = os.path.join(self.paths[type], path)

        if os.path.exists(path):
            return True
        else:
            return False

def loop():
    # Load Settings
    config_fn = getConfig()
    s = Settings(config_fn)

    server = ThreadedXMLRPCServer(("0.0.0.0", 49150))
    server.register_instance(Server(s))
    server.serve_forever()

def main():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # main loop
    loop()

if __name__ == '__main__':
    loop()
