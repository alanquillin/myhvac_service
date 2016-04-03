from Adafruit_CharLCD import Adafruit_CharLCD
from Adafruit_MCP230xx import MCP230XX_GPIO

# bus = 1         # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
# address = 0x20  # I2C address of the MCP230xx chip.
# gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.


class MCP23xxxDriver(object):
    def init(self, bus=1, address=0x20, gpio_count=8, **kwargs):
        # Create MCP230xx GPIO adapter.
        mcp = MCP230XX_GPIO(bus, address, gpio_count)

        # Create LCD, passing in MCP GPIO adapter.
        self._lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp)

        self._lcd.clear()


    def write(self, msg):
        self._lcd.message(msg)
