import cfg
import logging

LOG = logging.getLogger(__name__)

gpio_opts = [
    cfg.BoolOpt('fake', default=False, help='')
]

CONF = cfg.CONF
CONF.register_opts(gpio_opts, 'gpio')

# if not CONF.gpio.fake:
#     import RPi.GPIO as GPIO


def _fakify(fn, *args, **kwargs):
    if not CONF.gpio.fake:
        None
    return fn(*args, **kwargs)


BCM = "BCM"
BOARD = "BOARD"
IN = 1
OUT = 0


def setmode(*args, **kwargs):
    return None
    return GPIO.setmode(*args, **kwargs)


def setwarnings(*args, **kwargs):
    return None
    return GPIO.setwarnings(*args, **kwargs)


def setup(*args, **kwargs):
    return None
    return GPIO.setup(*args, **kwargs)


def input(*args, **kwargs):
    return None
    return GPIO.input(*args, **kwargs)


def output(*args, **kwargs):
    return None
    return output(*args, **kwargs)