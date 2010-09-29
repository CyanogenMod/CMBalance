from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.mirrors import Mirror
from pages.base import BasePage
import datetime
import logging
import re
import xmlrpclib

class TasksPage(BasePage):
    def _notify_mirrors(self):
        pymirrors = Mirror.all() \
                    .filter('control_type =', 'python') \
                    .fetch(100)

        for mirror in pymirrors:
            key = mirror.key()
            taskqueue.add(
                url="/tasks/notify_python_mirror",
                params={'key': key, 'ip': mirror.ip}
            )

        self.response.out.write("Done!")

    def _notify_python_mirror(self):
        ip = self.request.get('ip')
        try:
            s = xmlrpclib.Server("http://%s:49150" % ip)
            s.sync()
        except:
            pass

    def get(self):
        match = re.match("^/tasks/(.*)", self.request.path)
        if match:
            action = match.group(1)

        if action == "notify_mirrors":
            return self._notify_mirrors()

    def post(self):
        match = re.match("^/tasks/(.*)", self.request.path)
        if match:
            action = match.group(1)

        if action == "notify_python_mirror":
            return self._notify_python_mirror()

class PingMirrors(webapp.RequestHandler):
    def get(self):
        mirrors = Mirror.all().fetch(100)
        for mirror in mirrors:
            params = {
                'key': mirror.key(),
                'ip': mirror.ip,
                'control_type': mirror.control_type,
            }
            taskqueue.add(url='/tasks/ping_mirrors', params=params)

        self.response.out.write("done")

    def post(self):
        ip = self.request.get('ip')
        key = self.request.get('key')
        control_type = self.request.get('control_type')

        if control_type == "python":
            return self._python_ping(key, ip)

    def _python_ping(self, key, ip):
        s = xmlrpclib.Server("http://%s:49150" % ip)
        try:
            pong = s.ping()
            logging.debug("PONG: Got '%s' from %s" % (pong, ip))
            if pong == "pong":
                online = True
            else:
                online = False
        except Exception, e:
            logging.debug("PONG: Got Exception: %s" % (e))
            online = False

        # Update Mirror
        mirror = Mirror.get(key)
        if online:
            mirror.status = "online"
            mirror.last_seen = datetime.datetime.now()
            mirror.enabled = True
        else:
            mirror.status = "offline"
            mirror.enabled = False

        mirror.put()

routes = [
    ('^/tasks/ping_mirrors$', PingMirrors),
    ('^/tasks/.*$', TasksPage),
]
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
