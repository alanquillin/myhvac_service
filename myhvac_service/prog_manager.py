from myhvac_core import cfg
from myhvac_core import hvac
from myhvac_core import system_state as states
from myhvac_service.display import api as display
from myhvac_service import hub
from myhvac_service.programs import factory as prog_fac

import random

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.IntOpt('sleep_seconds', default=300,
                help='The amount of time in seconds to wait before checking the program state'),
]
CONF = cfg.CONF
CONF.register_opts(opts, 'program_manager')


class ProgramManager(object):
    def __init__(self):
        self.is_active = False

    def start(self):
        self.is_active = True
        while self.is_active:
            self.run()
            hub.sleep(CONF.program_manager.sleep_seconds)

    def close(self):
        self.is_active = False
        pass

    def run(self):
        current_state = hvac.get_system_state()

        # This is temp until we pull from db
        current_temp = random.randint(68, 74)

        program = prog_fac.get_program()

        expected_state = program.get_state(current_temp)

        if current_state != expected_state:
            if expected_state == states.OFF:
                hvac.set_system_state(expected_state, current_state)

        display.update()
