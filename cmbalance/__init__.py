from cmbalance.cache import cache
from cmbalance.database import init_database
from cmbalance.resources import Root
from pyramid.config import Configurator
from sqlalchemy.engine import engine_from_config

def main(global_config, **settings):

    # Setup engine.
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_database(engine)

    # App Configuration
    config = Configurator(root_factory=Root, settings=settings)
    config.add_static_view('static', 'cmbalance:static')
    config.scan('cmbalance.views')

    # Return the generated WSGI application.
    return config.make_wsgi_app()

