from cmbalance.database import init_database
from cmbalance.resources import Root
from pyramid.config import Configurator
from sqlalchemy.engine import engine_from_config

def main(global_config, **settings):

    # Load engine from config.
    engine = engine_from_config(settings, 'sqlalchemy.')
    engine.echo = True

    # Initialize Database
    init_database(engine)

    # App Configuration
    config = Configurator(root_factory=Root, settings=settings)

    # Add static content view.
    config.add_static_view('static', 'cmbalance:static')

    # Scan for view_config decorators.
    config.scan('cmbalance.views')

    # Return the generated WSGI application.
    return config.make_wsgi_app()

