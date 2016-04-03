import lcddriver


class Lcd2004Driver(object):
    def init(self, **kwargs):
        self._lcd = lcddriver.lcd()


    def write(self, msg):
        self._lcd.lcd_clear()

        # now we can display some characters (text, line)
        self._lcd.lcd_display_string(msg, 1)
        #self._lcd.lcd_display_string("      I am", 2)
        #self._lcd.lcd_display_string("        a", 3)
        #self._lcd.lcd_display_string("   Raspberry Pi !", 4)
