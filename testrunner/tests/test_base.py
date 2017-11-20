import json
import tempfile
import unittest
import falcon.testing

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from testrunner.models import Base
from testrunner import main


class BaseTestCase(unittest.TestCase):
    def tearDown(self):
        self.db_session.close()
        self.db_engine.dispose()

    def setUp(self):
        super(BaseTestCase, self).setUp()

        Session = sessionmaker()

        self.db_file = tempfile.NamedTemporaryFile()
        self.dsn = 'sqlite:///{0}'.format(self.db_file.name)
        self.db_engine = create_engine(self.dsn, echo=True)
        self.db_session = Session(bind=self.db_engine)

        self.app = main({}, **{'sqlalchemy.url': self.dsn})
        self.srmock = falcon.testing.StartResponseMock()

        Base.metadata.create_all(self.db_engine)

    def simulate_request(self, path, *args, **kwargs):
        env = falcon.testing.create_environ(path=path, **kwargs)
        return self.app(env, self.srmock)

    def assertOK(self, response, body=None):
        self.assertEqual(self.srmock.status, '200 OK')
        if body is not None and isinstance(body, dict):
            self.assertEqual(json.loads(response.decode('utf-8')), body)

    def assertCreated(self, response, body=None):
        self.assertEqual(self.srmock.status, '201 Created')
        if body is not None and isinstance(body, dict):
            self.assertEqual(json.loads(response.decode('utf-8')), body)
