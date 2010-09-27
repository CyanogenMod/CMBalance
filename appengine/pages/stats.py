from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from pages.base import BasePage

class StatsPage(BasePage):
    def get(self):
        self.response.out.write("hi")

routes = [
    ('^/stats$', StatsPage),
]
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
