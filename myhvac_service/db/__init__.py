from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myhvac_service import cfg
from myhvac_service.db import models
from myhvac_service.db.measurements import *
from myhvac_service.db.rooms import *
from myhvac_service.db.sensors import *

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('connection_string', required=True,
               help='Database connection string.  Ex: mysql://user:pass@localhost:port/database')
]

CONF = cfg.CONF
CONF.register_opts(opts, 'db')

engine = None
Session = None


def init_db():
    global engine, Session

    LOG.debug('Database connection string: %s', CONF.db.connection_string)

    engine = create_engine(CONF.db.connection_string)
    Session = sessionmaker()
    Session.configure(bind=engine)


def sessionize(f, *args, **kwargs):
    session = Session()

    ret = None
    try:
        ret = f(session, *args, **kwargs)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return ret