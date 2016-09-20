from myhvac_service import cfg
from myhvac_service.display.default import NullDisplay
from myhvac_service import system_state as states

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('default_format', default="Mode: %(mode)s\nCurrent Temp: %(temp_f).1fF\n              %(temp_c).1fC",
                help='The display type.'),
    cfg.StrOpt('type', default="lcd",
               help='The display type.')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'display')


class Display(object):
    def __init__(self):
        LOG.debug('Display type: %s', CONF.display.type)

        self._format = CONF.display.default_format
        self._display = self._get_display()
        self._data = dict(mode=states.print_state(states.UNKNOWN),
                          temp_f=0,
                          temp_c=0)

    def write(self, msg):
        self._display.write(msg)

    def write_default(self, **kwargs):
        self._data.update(**kwargs)
        self._display.write(self._format % self._data)

    def clear(self):
        self._display.clear()

    @staticmethod
    def _get_display():
        try:
            if CONF.display.type == 'lcd':
                from myhvac_service.display.lcd import LcdDisplay
                return LcdDisplay()
        except Exception as e:
            LOG.exception('There was an error trying to build the display driver \'%s\'.  '
                          'Using null display driver instead. Error: %s', CONF.display.type, e.message)
            return NullDisplay()

        LOG.info('Invalid display type set \'%s\'.  Using null display driver instead.', CONF.display.type)
        return NullDisplay()

display = None


def write(msg):
    display.write(msg)


def update(**kwargs):
    display.write_default(**kwargs)


def clear():
    display.clear()


def init_display():
    global display
    display = Display()
