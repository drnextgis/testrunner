import json
import unittest

from io import StringIO

from pkg_resources import resource_filename

from huey.contrib.sqlitedb import SqliteHuey

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    )

from .models import (
    StateEnum,
    Environment,
    Request,
    )


# Huey is a little task queue. SqliteHuey is implemented in such a
# way that it can safely be used with a multi-process, multi-thread,
# or multi-greenlet consumer.
huey = SqliteHuey('testrunner', filename=resource_filename(
    __name__, 'huey.db'))


# TODO: should be extracted from paste ini config file
db_url = 'sqlite:///%s' % resource_filename(
    __name__, 'testrunner.db')


# It is very important that web application does not use the
# same database session as Huey application.
DBSession = scoped_session(sessionmaker())


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@huey.task()
def run_test(request_id):
    request = DBSession.query(Request) \
        .filter_by(id=request_id).one()

    # if environment is busy create task with the same
    # args but 60 second delayed
    if request.environment.busy:
        run_test.schedule(args=(request_id,), delay=60)
        return

    # mark environment as busy
    request.environment.busy = True
    DBSession.commit()

    # tests here are "dotted names" that may resolve either to a module,
    # a test case class, a test method within a test case class,
    # a TestSuite instance, or a callable object which returns a
    # TestCase or TestSuite instance
    tests = json.loads(request.files)

    # setup unittest runner
    buf = StringIO()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(tests)
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)

    result = runner.run(suite)
    if result.wasSuccessful():
        request.state = StateEnum.SUCCESS
    else:
        request.state = StateEnum.FAILURE

    buf.seek(0)
    request.output = buf.getvalue()
    request.environment.busy = False

    DBSession.commit()


# Huey database session is only configured once
# during Huey initialization.
@huey.pre_execute()
@run_once
def initialize_session(run_test):
    engine = create_engine(db_url)
    DBSession.configure(bind=engine)
