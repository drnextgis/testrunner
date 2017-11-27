import json

from falcon.errors import HTTPConflict

from falcon_autocrud.resource import (
    CollectionResource,
    SingleResource,
    )

from sqlalchemy.orm.exc import NoResultFound

from .middlewares import Jinja2Response

from .models import (
    Environment,
    Request,
    )

from .consumer import run_test


class HomeResource:
    def on_get(self, req, resp):
        resp.context['template'] = Jinja2Response('home.jinja2')


class TestCollectionResource:
    def __init__(self, config):
        self.config = config

    def on_get(self, req, resp):
        result = []

        if self.config is not None:
            with open(self.config, 'r') as config:
                tests = json.load(config)
                result = tests.get('items')

        resp.body = json.dumps(result)


class EnvironmentResource(SingleResource):
    model = Environment
    methods = ['GET']


class EnvironmentCollectionResource(CollectionResource):
    model = Environment
    methods = ['GET', 'POST']


class RequestResource(SingleResource):
    model = Request
    methods = ['GET']


class RequestCollectionResource(CollectionResource):
    model = Request
    methods = ['GET', 'POST']

    def before_post(self, req, resp, db_session, request):
        try:
            environment = db_session.query(Environment) \
                .filter_by(id=request.environment_id).one()

        except NoResultFound:
            db_session.rollback()
            raise HTTPConflict('Conflict', 'Environment ID #%s not exist.' % (
                request.environment_id))

    def after_post(self, req, resp, request):
        run_test(request.id)
