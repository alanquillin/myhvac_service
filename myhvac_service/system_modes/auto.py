from myhvac_service import db
from myhvac_service.db import system
from myhvac_service import system_state as states
from myhvac_service.system_modes import SystemModeBase
from myhvac_service import utils

import logging

LOG = logging.getLogger(__name__)


class AutoMode(SystemModeBase):
    def __init__(self, id_, program):
        super(AutoMode, self).__init__(id_)
        self._set_program_name(program)

    @classmethod
    def name(cls):
        return 'Auto'

    def get_state(self, current_temp):
        def do(session):
            system_settings = system.get_current_system_settings(session)
            program = system_settings.current_program

            self._set_program_name(program)

            if not program:
                LOG.warn('No program set for system.')
                return states.OFF
            elif not program.schedules:
                LOG.warn('No schedules found for program \'%s\'.  Setting system to Off', program.name)
                return states.OFF

            schedule = utils.get_active_schedule(program)
            if not schedule:
                LOG.error('Could not determine the ')
            return self._get_state(current_temp, schedule.cool_temp, schedule.heat_temp)

        return db.sessionize(do)

    def program_name(self):
        return "%s (%s)" % (self._program_name, self.name())

    def _set_program_name(self, program):
        self._program_name = 'Unknown'

        if program:
            self._program_name = program.name
