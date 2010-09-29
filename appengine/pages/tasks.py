from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.mirrors import Mirror
from pages.base import BasePage
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

        self.response.out.write("Notify Python Mirror")

    def get(self):
        match = re.match("^/tasks/(.*)", self.request.path)
        if match:
            action = match.group(1)

        if action == "notify_mirrors":
            return self._notify_mirrors()

        self.response.out.write("hello world: %s" % action)

    def post(self):
        match = re.match("^/tasks/(.*)", self.request.path)
        if match:
            action = match.group(1)

        if action == "notify_python_mirror":
            return self._notify_python_mirror()

routes = [
    ('^/tasks/.*$', TasksPage),
]
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
