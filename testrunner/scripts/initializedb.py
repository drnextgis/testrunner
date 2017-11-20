import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    )

from testrunner.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    Environment,
    Base,
    )

DBSession = scoped_session(sessionmaker())


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    settings = get_appsettings(config_uri)

    if 'logging' in settings:
        setup_logging(settings.get('logging'))

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    # create 100 dummy environments
    for i in range(1, 101):
        try:
            DBSession.query(Environment).filter_by(id=i).one()
        except NoResultFound:
            environment = Environment(name='environment %d' % i)
            DBSession.add(environment)

    DBSession.commit()
