from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.base import Constants
from model.files import File
from pages.base import BasePage

class BrowsePage(BasePage):
    def get(self):
        return self._handlePage("index")

    def index(self):
        type = self.request.get('type', None)
        device = self.request.get('device', None)
        title = "Recent Files"

        files = File.all()

        if type:
            files = files.filter('type =', type)
            title = 'Browse Files - %s' % type

        if device:
            files = files.filter('device =', device)
            title = 'Browse Files - %s' % device

        if device and type:
            title = "Browse Files - %s / %s" % (device, type)

        values = {
            'files': files.order('-date_created').fetch(limit=30),
            'devices': Constants.cache(key_name='devices'),
            'types': Constants.cache(key_name='types'),

            'title': title,
        }
        self.render(values)

def main():
    routes = [('/', BrowsePage)]
    application = webapp.WSGIApplication(routes, debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
