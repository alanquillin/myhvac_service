import lcd2004


class Lcd2004Driver(object):
    def __init__(self, **kwargs):
        self._lcd = lcd2004.lcd()

    def write(self, msg):
        self.clear()

        # now we can display some characters (text, line)
        lines = msg.split('\n')
        cnt = 1
        for line in lines:
            if cnt > 4:
                break

            self._lcd.lcd_display_string(line, cnt)
            cnt = cnt + 1

    def clear(self):
        self._lcd.lcd_clear()