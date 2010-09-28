from google.appengine.api import memcache
from model.files import File
from model.mirrors import Mirror
import os.path
import urlparse

def getDownloadURL(device, filename):
    file = memcache.get("file_%s_%s" % (device, filename))
    if file is None:
        file = File.all() \
                .filter('device =', device) \
                .filter('filename =', filename).get()
        memcache.set("file_%s_%s" % (device, filename), file, 60)

    mirror = getNextMirror()
    url = urlparse.urlunparse((
                mirror.scheme,
                mirror.netloc,
                os.path.join(mirror.path, file.type, file.path),
                mirror.params,
                mirror.query,
                mirror.fragment))
    return url

def getNextMirror():
    checkMirrorHitsLength()
    mirror_hits = memcache.get('mirror_hits')
    if mirror_hits is None:
        mirror_hits = generateMirrorHits()

    mirror_hits.sort()
    mirror_hits[0][0] += 1
    memcache.set('mirror_hits', mirror_hits, 60)
    mirror = Mirror.get(mirror_hits[0][1])
    return urlparse.urlparse(mirror.url)

def generateMirrorHits():
    mirror_hits = []

    mirrors = Mirror.all().filter('enabled =', True).fetch(1000)
    for mirror in mirrors:
        mirror_hits.append([0, str(mirror.key())])

    memcache.set('mirror_hits', mirror_hits, 60)

    return mirror_hits

def checkMirrorHitsLength():
    mh = memcache.get('mirror_hits')
    if mh is None:
        mh = 0
    mirrors_count = Mirror.all().filter('enabled =', True).count()
    mirror_hits = len(mh)

    if mirrors_count != mirror_hits:
        generateMirrorHits()
