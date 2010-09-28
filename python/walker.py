from utils import AndroidBuild
import os
import re
import time
import urllib

RE_ZIP = re.compile(r'^update-cm-6(.*)-signed.zip$')
PATH = "/home/ctso/cmstable"

def walk():
    builds = []

    path = os.walk(PATH)
    for root, dirs, files in path:
        for name in files:
            if RE_ZIP.match(name):
                fn = os.path.join(root, name)
                builds.append(fn)

    for build in builds:
        createRecord(build)

def createRecord(build):
    zip = AndroidBuild(build)

    server_path = re.match(r'%s/(.*)' % PATH, build).group(1)
    filename = os.path.basename(server_path)
    device = zip.device
    size = zip.size
    date = str(zip.build_date).replace('CEST', 'UTC')
    date = time.mktime(time.strptime(date, "%a %b %d %H:%M:%S %Z %Y"))

    values = {
        'key': 'master',
        'action': 'addFile',
        'path': server_path,
        'filename': filename,
        'device': device,
        'size': size,
        'date_created': date,
        'type': 'stable',
    }
    values = urllib.urlencode(values)

    url = "http://cmbalance.appspot.com/rpc?%s" % values
    #urllib.urlopen(url).read()
    print url

    print "Adding %s" % filename

if __name__ == '__main__':
    walk()
