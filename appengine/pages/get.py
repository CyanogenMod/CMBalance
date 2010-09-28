from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.download import getDownloadURL
from pages.base import BasePage
import re

class GetPage(BasePage):
    def get(self):
        match = re.match(r'^/get/(.*)/(.*)$', self.request.path)
        if match:
            device = match.group(1)
            filename = match.group(2)
        else:
            return self._invalidRequest()

        url = getDownloadURL(device, filename)
        self.redirect(url, True)

routes = [
    ('^/get/.*$', GetPage),
]
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
