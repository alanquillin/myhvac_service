from smbus import SMBus
# RPi.GPIO compatible interface for PCF8574
# Only supports output
class Pcf8574Gpio(object):
    BCM = 0
    OUT = 0
    def __init__(self, busnum, address):
        self.bus = SMBus(busnum)
        self.address = address
        # Set all outputs off
        self.bus.write_byte(self.address, 0x00)
        # Store P-port state
        self.byte = 0x00
    
    def _changebit(self, bit, new_value):
        if new_value == 0:
            self.byte &= ~(1 << bit)
        elif new_value == 1:
            self.byte |= (1 << bit)

    def output(self, pin, value):
        self._changebit(pin, value)
        self.bus.write_byte(self.address, self.byte)

    def setmode(self, mode):
        pass
    
    def setup(self, pin, mode):
        pass

    def cleanup(self):
        # Set all outputs off
        self.bus.write_byte(self.address, 0x00)
