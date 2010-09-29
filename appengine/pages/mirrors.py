from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.mirrors import Mirror, MirrorHits
from pages.base import BasePage

class MirrorsPage(BasePage):
    def get(self):
        return self._handlePage("index")

    def index(self):
        values = self.values

        mirrors = Mirror.all().fetch(100)
        for mirror in mirrors:
            if mirror.link is None:
                mirror.link = "http://mirror.teamdouche.net/mirrors"
                if mirror.status == "offline":
                    mirror.icon = "exclamation.png"
                if mirror.status == "online":
                    mirror.icon = "accept.png"

            hits = MirrorHits.get_by_key_name(str(mirror.key()))
            mirror.hits = hits.count

        values.update({
            'mirrors': mirrors,
        })

        self.render(values)

def main():
    routes = [('/mirrors', MirrorsPage)]
    application = webapp.WSGIApplication(routes, debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
