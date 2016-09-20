from myhvac_service import cfg
from myhvac_service.display.drivers.lcds.lcd2004_driver import Lcd2004Driver

import logging

LOG = logging.getLogger(__name__)

opts = [

]

lcd_opts = [
    cfg.IntOpt('bus', default=1, help=''),
    cfg.IntOpt('address', default=0x27, help=''),
    cfg.IntOpt('gpio_count', default=8, help=''),
    cfg.StrOpt('driver', default="lcd2004",
               help='The amount of time in seconds to wait before checking the program state'),
]

CONF = cfg.CONF
CONF.register_opts(lcd_opts, 'lcd')


class LcdDisplay(object):
    def __init__(self):
        LOG.debug('LCD configs:')
        LOG.debug('Bus: %s', CONF.lcd.bus)
        LOG.debug('Address: %s', CONF.lcd.address)
        LOG.debug('GPIO Count: %s', CONF.lcd.gpio_count)
        LOG.debug('Driver: %s', CONF.lcd.driver)

        if CONF.lcd.driver == 'lcd2004':
            self._driver = Lcd2004Driver()

    def write(self, msg):
        self._driver.write(msg)

    def clear(self):
        self._driver.clear()