from pyramid.config import Configurator
from cmbalance.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('cmbalance.views.my_view',
                    context='cmbalance:resources.Root',
                    renderer='cmbalance:templates/mytemplate.pt')
    config.add_static_view('static', 'cmbalance:static')
    return config.make_wsgi_app()

