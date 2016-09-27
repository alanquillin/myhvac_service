from Adafruit_CharLCD import Adafruit_CharLCD
from Adafruit_MCP230xx import MCP230XX_GPIO

from myhvac_service import cfg

CONF = cfg.CONF


class MCP23xxxDriver(object):
    def __init__(self, **kwargs):
        # Create MCP230xx GPIO adapter.
        mcp = MCP230XX_GPIO(CONF.lcd.bus, CONF.lcd.address, CONF.lcd.gpio_count)

        # Create LCD, passing in MCP GPIO adapter.
        self._lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp)

        self._lcd.clear()


    def write(self, msg):
        self.clear()
        self._lcd.message(msg)

    def clear(self):
        self._lcd.clear()
