from exc import DuplicateRecordException
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.files import File
from model.mirrors import Mirror

class RPCHandler(webapp.RequestHandler):
    blacklist = ['get', 'post']

    def _checkAccess(self):
        action = self.request.get('action')
        key = self.request.get('key')

        if action.startswith("_") or action in self.blacklist:
            return self._denyAccess()

        if key == "master":
            return True

        if key:
            m = Mirror.cache(key)
            if m.ip == self.request.remote_addr:
                return self._checkEnabled()

        return False

    def _checkEnabled(self):
        key = self.request.get('key')
        if key:
            m = Mirror.cache(key)
            if m.enabled:
                return True

        return False

    def _denyAccess(self):
        self.error(403)
        self.response.out.write("403 - Access Denied")

    def _invalidRequest(self):
        self.error(400)
        self.response.out.write("400 - Bad Request")

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
        }

        for value in values.itervalues():
            if value is None:
                return self._invalidRequest()

        try:
            file = File.check(**values)
            file.put()
        except DuplicateRecordException:
            self._invalidRequest()

    def heartbeat(self):
        key = self.request.get('key')
        m = Mirror.cache(key)
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
