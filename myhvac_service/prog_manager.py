from myhvac_service import cfg
from myhvac_service import hub
from myhvac_service import display
from myhvac_service import hvac
from myhvac_service.programs import factory as prog_fac
from myhvac_service import system_state as states
from myhvac_service import temp

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

        current_state, _ = hvac.get_system_state()
        if current_state != states.OFF:
            hvac.set_system_state(states.OFF, current_state)

    def run(self):
        try:
            LOG.debug('Running program interval...')
            current_state, _ = hvac.get_system_state()
            LOG.debug('Current state: %s', states.print_state(current_state))

            current_temp = temp.get_current_temp()
            if not current_temp:
                LOG.error('Bailing out of current progam run... No temp data found.  Setting system state to OFF')
                hvac.set_system_state(states.OFF, current_state)
                return

            current_temp_c = (current_temp - 32) * 5.0 / 9.0
            LOG.debug('Current temp: %s', current_temp)

            program = prog_fac.get_program()
            LOG.debug('Running program %s, program type %s', program.name, program.get_program_type())

            expected_state = program.get_state(current_temp)
            LOG.debug('Expected state: %s', states.print_state(expected_state))

            if current_state != expected_state:
                LOG.info('Setting system state to: %s', states.print_state(expected_state))
                hvac.set_system_state(expected_state, current_state)
            else:
                LOG.debug('Seems like the system is already in the expected state, so I ain\'t gonna do crap!')

            display.update(mode=states.print_state(expected_state),
                           temp_f=current_temp,
                           temp_c=current_temp_c)
        except Exception:
            LOG.exception('CRAP!!!! Stuff happened')
