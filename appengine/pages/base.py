from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import inspect
import os.path
import re

class BasePage(webapp.RequestHandler):
    values = {
        'devices': ['bravo', 'dream_sapphire', 'espresso', 'hero', 'heroc', 'inc', 'liberty', 'legend', 'passion', 'sholes', 'supersonic', 'various'],
        'types': ['stable', 'nightly', 'gapps'],
    }

    def _denyAccess(self):
        self.error(403)
        self.response.out.write("403 - Access Denied")

    def _invalidRequest(self):
        self.error(400)
        self.response.out.write("400 - Bad Request")

    def _getTemplate(self):
        cls = self.__class__.__name__
        folder = re.match("^(.*)Page$", cls)
        if folder:
            folder = folder.group(1).lower()
        else:
            raise Exception()

        action = inspect.stack()[2][3]

        filename = os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        'templates', folder,
                        "%s.html" % action)

        return filename

    def _handlePage(self, page):
        func = "%s" % page

        try:
            func = self.__getattribute__(func)
            func()
        except AttributeError:
            self.response.set_status(404)

    def render(self, values={}):
        tpl = self._getTemplate()

        content = template.render(tpl, values)
        content = content.replace('\n', '')
        content = content.replace('\t', '')

        self.response.out.write(content)
