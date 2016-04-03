from myhvac_core import cfg
from myhvac_service.display.drivers.lcds.lcd2004_driver import Lcd2004Driver

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('lcd_driver', default="lcd2004",
                help='The amount of time in seconds to wait before checking the program state'),
]
CONF = cfg.CONF
CONF.register_opts(opts, 'display')


class LcdDriver(object):
    def __init__(self):
        if CONF.display.lcd_driver == 'lcd2004':
            self._driver = Lcd2004Driver()

    def write(self, msg):
        self._driver.write(msg)