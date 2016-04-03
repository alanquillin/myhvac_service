from myhvac_core import cfg
from myhvac_service.display.drivers.lcd import LcdDriver

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('type', default="lcd",
                help='The amount of time in seconds to wait before checking the program state'),
]
CONF = cfg.CONF
CONF.register_opts(opts, 'display')

driver_types = dict(lcd=LcdDriver())

def get_driver():
    return driver_types[CONF.display.type]