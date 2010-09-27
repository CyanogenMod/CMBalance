from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from pages.base import BasePage
import re

class AdminPage(BasePage):
    def index(self):
        self.render()

    def get(self):
        page = re.match(r'^/admin/(.*)\.html$', self.request.path)
        if page:
            page = page.group(1)
            return self._handlePage(page)
        else:
            return self.redirect('/admin/index.html')

routes = [
    ('^/admin$', AdminPage),
    ('^/admin/.*\.html$', AdminPage),
]
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
