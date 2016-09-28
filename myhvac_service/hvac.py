import cfg
import logging

import threading

from myhvac_service import gpio as GPIO
from myhvac_service import system_state as state

LOG = logging.getLogger(__name__)

io_opts = [
    cfg.IntOpt('green_pin_out', required=True, help='GPIO pin output number for green (FAN) wire'),
    cfg.IntOpt('green_pin_fb', required=True, help='GPIO pin feedback number for green (FAN) wire'),
    cfg.IntOpt('green_pin_lb', required=True, help='GPIO pin loopback number for green (FAN) wire'),
    cfg.IntOpt('white_pin_out', required=True, help='GPIO pin output number for white (HEAT) wire'),
    cfg.IntOpt('white_pin_fb', required=True, help='GPIO pin feedback number for white (HEAT) wire'),
    cfg.IntOpt('white_pin_lb', required=True, help='GPIO pin loopback number for white (HEAT) wire'),
    cfg.IntOpt('yellow_pin_out', required=True, help='GPIO pin output number for yellow (COOL) wire'),
    cfg.IntOpt('yellow_pin_fb', required=True, help='GPIO pin feedback number for yellow (COOL) wire'),
    cfg.IntOpt('yellow_pin_lb', required=True, help='GPIO pin loopback number for yellow (COOL) wire'),
    cfg.StrOpt('pin_mode', required=True, help='GPIO pin mode.  Available values: [board, bcm]')
]

hvac_opts = [
    cfg.IntOpt('on_mode_change_fan_interval', default=120,
               help='The time (in seconds) to run FAN_ONLY mode before changing the system mode.')
]

CONF = cfg.CONF
CONF.register_opts(io_opts, 'io')
CONF.register_opts(hvac_opts, 'hvac')


def init_gpio():
    mode = GPIO.BCM
    if CONF.io.pin_mode.lower() == 'board':
        mode = GPIO.BOARD

    GPIO.setmode(mode)
    GPIO.setwarnings(False)
    GPIO.setup(CONF.io.green_pin_out, GPIO.OUT)
    GPIO.setup(CONF.io.green_pin_fb, GPIO.IN)
    GPIO.setup(CONF.io.green_pin_lb, GPIO.IN)
    GPIO.setup(CONF.io.white_pin_out, GPIO.OUT)
    GPIO.setup(CONF.io.white_pin_fb, GPIO.IN)
    GPIO.setup(CONF.io.white_pin_lb, GPIO.IN)
    GPIO.setup(CONF.io.yellow_pin_out, GPIO.OUT)
    GPIO.setup(CONF.io.yellow_pin_fb, GPIO.IN)
    GPIO.setup(CONF.io.yellow_pin_lb, GPIO.IN)


def get_system_state():
    def _get_state(gp, wp, yp):
        state_ = state.UNKNOWN
        is_green_on = GPIO.input(gp)
        is_white_on = GPIO.input(wp)
        is_yellow_on = GPIO.input(yp)

        if is_green_on and is_white_on and is_yellow_on:
            state_ = state.COOL

        elif is_green_on and is_white_on and not is_yellow_on:
            state_ = state.HEAT

        elif is_green_on and not is_white_on and not is_yellow_on:
            state_ = state.FAN_ONLY

        elif not is_green_on and not is_white_on and not is_yellow_on:
            state_ = state.OFF

        return state_

    return (_get_state(CONF.io.green_pin_fb, CONF.io.white_pin_fb, CONF.io.yellow_pin_fb),
            _get_state(CONF.io.green_pin_lb, CONF.io.white_pin_lb, CONF.io.yellow_pin_lb))


def set_system_state(to_state, current_state):
    if to_state == state.UNKNOWN:
        LOG.error('Trying to set system status UNKNOWN.... Uncool... bailing.  Current state: %s',
                  state.print_state(current_state))
        return

    def _set_system_state(s):
        LOG.info('Setting system mode: %s', state.print_state(s))
        if s == state.HEAT:
            _heat_on()
        elif s == state.COOL:
            _cool_on()
        elif s == state.FAN_ONLY:
            _fan_only()
        elif s == state.OFF:
            _off()

        # Verify that the system state was set currently
        threading._sleep(1)
        cs, _ = get_system_state()
        if s != cs:
            LOG.error('The system state was not set correctly!  Expected state: %s, Actual state: %s',
                      state.print_state(s), state.print_state(cs))

    def _heat_on():
        GPIO.output(CONF.io.green_pin_out, True)
        GPIO.output(CONF.io.white_pin_out, True)
        GPIO.output(CONF.io.yellow_pin_out, False)

    def _cool_on():
        GPIO.output(CONF.io.green_pin_out, True)
        GPIO.output(CONF.io.white_pin_out, True)
        GPIO.output(CONF.io.yellow_pin_out, True)

    def _fan_only():
        GPIO.output(CONF.io.green_pin_out, True)
        GPIO.output(CONF.io.white_pin_out, False)
        GPIO.output(CONF.io.yellow_pin_out, False)

    def _off():
        GPIO.output(CONF.io.green_pin_out, False)
        GPIO.output(CONF.io.white_pin_out, False)
        GPIO.output(CONF.io.yellow_pin_out, False)

    if current_state in [state.OFF, state.FAN_ONLY]:
        _set_system_state(to_state)
    else:
        # First set the system to fan only to let the system cool down for 2 minutes, then set the system state
        _set_system_state(state.FAN_ONLY)
        threading._sleep(CONF.hvac.on_mode_change_fan_interval)
        _set_system_state(to_state)
