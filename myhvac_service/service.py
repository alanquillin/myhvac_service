from myhvac_core import cfg
from myhvac_core import hvac
from myhvac_service.display import api as display
from myhvac_service import hub
from myhvac_service import prog_manager as pm
from myhvac_service.rest import app

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.BoolOpt('debug', default=False,
                help='Enables debug mode for the flask rest api'),
    cfg.IntOpt('port', default=8080, help='Http port of the webserver')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'rest_api')


def main():
    display.write('Starting up system...')
    hvac.init_gpio()

    prog_man = pm.ProgramManager()

    try:
        hub.joinall([hub.spawn(prog_man.start),
                     hub.spawn(app.run(debug=CONF.rest_api.debug,
                                       port=CONF.rest_api.port,
                                       use_reloader=False))])
    finally:
        prog_man.close()
