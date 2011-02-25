from cmbalance.cache import cache
from cmbalance.database import init_database, DBSession
from cmbalance.resources import Root
from pyramid.config import Configurator
from sqlalchemy.engine import engine_from_config

class SessionFixMiddleware(object):
    """
    Hackish middleware to fix my SQLA noobness.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        session = DBSession()
        try:
            return self.app(environ, start_response)
        except:
            session.rollback()
        finally:
            session.close()
            DBSession.remove()

def main(global_config, **settings):

    # Setup engine.
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_database(engine)

    # App Configuration
    config = Configurator(root_factory=Root, settings=settings)
    config.add_static_view('static', 'cmbalance:static')
    config.scan('cmbalance.views')

    app = SessionFixMiddleware(config.make_wsgi_app())

    # Return the generated WSGI application.
    return app

