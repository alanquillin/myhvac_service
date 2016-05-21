from myhvac_core import cfg
from myhvac_core import hvac
from myhvac_core import hub
from myhvac_core import system_state as states
from myhvac_service.display import api as display
from myhvac_service.programs import factory as prog_fac

import random
import logging
from datetime import datetime
from datetime import timedelta

LOG = logging.getLogger(__name__)

opts = [
    cfg.IntOpt('sleep_seconds', default=300,
                help='The amount of time in seconds to wait before checking the program state'),
]
CONF = cfg.CONF
CONF.register_opts(opts, 'program_manager')


class ProgramManager(object):
    __instance = None

    is_active = False
    is_running = False

    def __new__(cls):
        if ProgramManager.__instance is None:
            ProgramManager.__instance = object.__new__(cls)

        return ProgramManager.__instance

    def start(self):
        LOG.info('Starting Program Manager')
        LOG.debug('Interval sleep time: %s (seconds)', CONF.program_manager.sleep_seconds)
        self.is_active = True
        self.is_running = True

        next_run = datetime.min
        while self.is_active:
            if datetime.now() > next_run:
                self.run()
                next_run = datetime.now() + timedelta(seconds=CONF.program_manager.sleep_seconds)
            hub.sleep(1)

        self.is_running = False

    def close(self):
        LOG.info('Stopping Program Manager')
        self.is_active = False

        while self.is_running:
            hub.sleep(1)

        current_state = hvac.get_system_state()
        if current_state != states.OFF:
            hvac.set_system_state(states.OFF, current_state)

    def run(self):
        LOG.debug('Running program interval...')
        current_state = hvac.get_system_state()
        LOG.debug('Current state: %s', states.print_state(current_state))
        # This is temp until we pull from db
        current_temp_c = random.randint(19, 24)
        current_temp = current_temp_c * 1.8 + 32
        LOG.debug('Current temp: %s', current_temp)
        program = prog_fac.get_program()

        expected_state = program.get_state(current_temp)
        LOG.debug('Expected state: %s', states.print_state(expected_state))
        if current_state != expected_state:
            LOG.info('Setting system state to: %s', states.print_state(expected_state))
            hvac.set_system_state(expected_state, current_state)

        display.update(mode=states.print_state(expected_state),
                       temp_f=current_temp,
                       temp_c=current_temp_c)
