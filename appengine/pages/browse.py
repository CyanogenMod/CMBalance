from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.files import File
from pages.base import BasePage
import urllib

class BrowsePage(BasePage):
    def get(self):
        return self._handlePage("index")

    def _make_webconnect(self, file):
        querystring = {
            'data.url': "http://mirror.teamdouche.net/get/%s/%s" % (file.device, file.filename),
            'data.name': file.filename,
            'success_redirect': 'http://mirror.teamdouche.net/rommanager?success=true',
            'failure_redirect': 'http://mirror.teamdouche.net/rommanager?success=false',
            'applicationId': 'ROM Manager',
        }
        url = 'https://tickleservice.appspot.com/authorizedtickle?%s' % urllib.urlencode(querystring)
        return url

    def index(self):
        type = self.request.get('type', None)
        device = self.request.get('device', None)
        title = "Recent Files"
        link_nightly = {'type': 'nightly'}
        link_stable = {'type': 'stable'}

        files = File.all()

        if type:
            files = files.filter('type =', type)
            title = 'Browse Files - %s' % type

        if device:
            files = files.filter('device =', device)
            title = 'Browse Files - %s' % device
            link_stable.update({'device': device})
            link_nightly.update({'device': device})

        if device and type:
            title = "Browse Files - %s / %s" % (device, type)

        files = files.order('-date_created').fetch(limit=30)
        for file in files:
            file.tickle_url = self._make_webconnect(file)

        values = self.values
        values.update({
            'files': files,
            'title': title,
            'link_nightly': "/?" + urllib.urlencode(link_nightly),
            'link_stable': "/?" + urllib.urlencode(link_stable),
        })
        self.render(values)

def main():
    routes = [('/', BrowsePage)]
    application = webapp.WSGIApplication(routes, debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
