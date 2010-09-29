import os.path
import re
import zipfile

RE_BUILDPROP = re.compile(r'^(.*)=(.*)$')

class AndroidBuild(object):
    def __init__(self, file):
        self.file = file
        self.load_build_prop()

    def load_build_prop(self):
        fd = zipfile.ZipFile(self.file)
        bp = fd.read("system/build.prop")
        fd.close()

        self.build_prop = {}

        bp = bp.split("\n")
        for line in bp:
            m = RE_BUILDPROP.match(line)
            if m:
                self.build_prop.update({
                    m.group(1): m.group(2)
                })

    @property
    def size(self):
        return self.getSize()

    @property
    def device(self):
        return self.getDevice()

    @property
    def build_date(self):
        return self.getBuildDate()

    @property
    def build_host(self):
        return self.getBuildHost()

    @property
    def build_user(self):
        return self.getBuildUser()

    @property
    def modversion(self):
        return self.getModVersion()

    def getSize(self):
        return os.path.getsize(self.file)

    def getModVersion(self):
        return self.build_prop.get('ro.modversion', None)

    def getBuildUser(self):
        return self.build_prop.get('ro.build.user', None)

    def getBuildHost(self):
        return self.build_prop.get('ro.build.host', None)

    def getDevice(self):
        return self.build_prop.get('ro.product.device', None)

    def getBuildDate(self):
        return self.build_prop.get('ro.build.date', None)

if __name__ == '__main__':
    ab = AndroidBuild("/home/ctso/Downloads/cm_dream_sapphire-09252010-001901.zip")
