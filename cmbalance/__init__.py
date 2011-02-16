from pyramid.config import Configurator
from cmbalance.resources import Root

def main(global_config, **settings):

    # App Configuration
    config = Configurator(root_factory=Root, settings=settings)

    # Add static content view.
    config.add_static_view('static', 'cmbalance:static')

    # Scan for view_config decorators.
    config.scan('cmbalance.views')

    # Return the generated WSGI application.
    return config.make_wsgi_app()

