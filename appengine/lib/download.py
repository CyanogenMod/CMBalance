from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue
from model.files import File
from model.mirrors import Mirror
import logging
import os.path
import urlparse
import xmlrpclib

def getDownloadURL(device, filename):
    file = memcache.get("file_%s_%s" % (device, filename))
    if file is None:
        file = File.all() \
                .filter('device =', device) \
                .filter('filename =', filename).get()
        memcache.set("file_%s_%s" % (device, filename), file, 60)

    # Figure out the next mirror in the round robin.
    mirror = getNextMirror(file.type, file.path)
    url = urlparse.urlunparse((
                mirror.scheme,
                mirror.netloc,
                os.path.join(mirror.path, file.type, file.path),
                mirror.params,
                mirror.query,
                mirror.fragment))
    return url

def getNextMirror(type, path):
    mirror_hits = generateMirrorHits()
    mirror_hits.sort()

    # Update hit count.
    mirror_hits[0][0] += 1
    memcache.set('mirror_hits', mirror_hits, 60)

    # Load mirror object.
    mirror = Mirror.get(mirror_hits[0][1])

    # Make sure the mirror has the requested file.
    try:
        s = xmlrpclib.Server("http://%s:49150" % mirror.ip)
        fileExists = s.fileExists(type, path)
    except:
        fileExists = False

    if fileExists:
        # All is well, return this mirror.
        logging.debug("%s HAS %s/%s" % (mirror.ip, type, path))
        return urlparse.urlparse(mirror.url)
    else:
        # Mirror says it doesn't have the file!
        # Tell them all to sync, and move to the next mirror.
        logging.debug("%s does not have %s/%s!" % (mirror.ip, type, path))
        taskqueue.add(url='/tasks/notify_mirrors', method='get')
        return getNextMirror(type, path)

def generateMirrorHits():
    mirror_hits = memcache.get('mirror_hits')
    if mirror_hits is None:
        mirror_hits = []

        mirrors = Mirror.all().filter('enabled =', True).fetch(1000)
        for mirror in mirrors:
            mirror_hits.append([0, str(mirror.key())])

        memcache.set('mirror_hits', mirror_hits, 60)
    else:
        # Check for new mirrors
        mc = Mirror.all().filter('enabled =', True).count()
        if len(mirror_hits) != mc:
            # clear cache and run this function again
            memcache.set('mirror_hits', None, 60)
            return generateMirrorHits()

    return mirror_hits
