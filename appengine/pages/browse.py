from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.files import File
from pages.base import BasePage

class BrowsePage(BasePage):
    def get(self):
        return self._handlePage("index")

    def index(self):
        values = {
            'files': File.all().order('-date_created').fetch(limit=30),
        }
        self.render(values)

def main():
    routes = [('/', BrowsePage)]
    application = webapp.WSGIApplication(routes, debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
