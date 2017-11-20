import falcon

from falcon_autocrud.middleware import Middleware as CRUDMiddleware

from pkg_resources import resource_filename

from sqlalchemy import engine_from_config

from .paster import setup_logging

from .middlewares import (
    Jinja2Middleware,
    StaticsMiddleware,
    )

from .resources import (
    HomeResource,
    TestCollectionResource,
    EnvironmentCollectionResource,
    EnvironmentResource,
    RequestCollectionResource,
    RequestResource,
    )


def main(global_config, **settings):
    """ This function returns a Falcon WSGI application.
    """
    if 'logging' in settings:
        setup_logging(settings.get('logging'))

    # tests config
    tests = settings.get('tests')

    engine = engine_from_config(settings, 'sqlalchemy.')

    app = falcon.API(middleware=[
        CRUDMiddleware(),
        Jinja2Middleware(resource_filename(__name__, 'templates')),
        StaticsMiddleware(static_folder=resource_filename(__name__, 'static')),
    ])

    app.add_route('/', HomeResource())

    # REST API
    app.add_route('/api/environment/',
                  EnvironmentCollectionResource(engine))
    app.add_route('/api/environment/{id}',
                  EnvironmentResource(engine))
    app.add_route('/api/request/',
                  RequestCollectionResource(engine))
    app.add_route('/api/request/{id}',
                  RequestResource(engine))
    app.add_route('/api/test/', TestCollectionResource(tests))

    return app
