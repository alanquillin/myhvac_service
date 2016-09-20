from myhvac_service import cfg
from myhvac_service import db
from myhvac_service import display
from myhvac_service import hub
from myhvac_service import hvac
from myhvac_service import log
from myhvac_service import prog_manager as pm
from myhvac_service import wsgi

import logging
import os
import signal
import sys

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

threads = []


def on_exit(sig, func=None):
    prog_man = pm.ProgramManager()
    shutdown(prog_man)
    sys.exit(0)


def shutdown(prog_man):
    display.write('Shutting down...')
    LOG.info('Shutting down system...')
    wsgi.stop()
    prog_man.close()

    # Wait for all threads to shut down
    hub.joinall(threads)
    display.clear()


def main():
    try:
        CONF(project='myhvac_service')
    except cfg.RequiredOptError as e:
        print e
        CONF.print_help()
        raise SystemExit(1)

    log.init_log()
    display.init_display()

    LOG.info('Starting up system... pid: %s', os.getpid())
    display.write('Starting up system..')

    db.init_db()
    hvac.init_gpio()

    prog_man = pm.ProgramManager()

    try:
        threads.append(hub.spawn(wsgi.run))
        threads.append(hub.spawn(prog_man.start))

        # Keep main thread alive to capture kill events
        while True:
            hub.sleep(.1)
    except (KeyboardInterrupt, SystemExit):
        LOG.error('Caught KeyboardInterrupt, initiate shutdown')
    finally:
        shutdown(prog_man)

signal.signal(signal.SIGTERM, on_exit)

if __name__ == '__main__':
    main()
