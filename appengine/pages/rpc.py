from exc import DuplicateRecordException
from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.files import File
from model.mirrors import Mirror
from pages.base import BasePage
import datetime

class RPCHandler(BasePage):
    blacklist = ['get', 'post']

    def _checkAccess(self):
        action = self.request.get('action')
        key = self.request.get('key')

        if action.startswith("_") or action in self.blacklist:
            return self._denyAccess()

        if key == "master":
            return True

        if key:
            m = Mirror.cache(key=key)
            if m.ip == self.request.remote_addr:
                return self._checkEnabled()

        return False

    def _checkEnabled(self):
        key = self.request.get('key')
        if key:
            m = Mirror.cache(key=key)
            if m.enabled:
                return True

        return False

    def _processRequest(self):
        action = self.request.get('action')
        try:
            func = self.__getattribute__(action)
            return func()
        except AttributeError:
            self._denyAccess()

    def addFile(self):
        values = {
            'type': self.request.get('type', None),
            'device': self.request.get('device', None),
            'filename': self.request.get('filename', None),
            'path': self.request.get('path', None),
            'date_created': datetime.datetime.fromtimestamp(float(self.request.get('date_created', None))),
            'size': int(self.request.get('size', None)),
        }

        for value in values.itervalues():
            if value is None:
                return self._invalidRequest()

        try:
            file = File.check(**values)
            file.put()
            sync = True
        except DuplicateRecordException:
            sync = False
            self._invalidRequest()

        if sync:
            taskqueue.add(url='/tasks/notify_mirrors', method='get')

    def addMirror(self):
        values = {
            'owner': self.request.get('owner', None),
            'url': self.request.get('url', None),
            'ip': self.request.get('ip', None),
            'control_type': self.request.get('control_type', None),
        }

        for value in values.itervalues():
            if value is None:
                return self._invalidRequest()

        mirror = Mirror(**values)
        mirror.put()

    def heartbeat(self):
        key = self.request.get('key')
        m = Mirror.cache(key=key)
        m.put()
        self.response.out.write("pong")

    def get(self):
        if self._checkAccess():
            return self._processRequest()
        else:
            return self._denyAccess()

def main():
    routes = [('/rpc', RPCHandler)]
    application = webapp.WSGIApplication(routes, debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
