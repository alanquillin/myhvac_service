from myhvac_service import db
from myhvac_service.db import system
from myhvac_service import system_state as states
from myhvac_service.programs import ProgramBase
from myhvac_service import utils

import logging

LOG = logging.getLogger(__name__)


class AutoProgram(ProgramBase):
    def __init__(self, id_):
        super(AutoProgram, self).__init__(id_)


    @classmethod
    def name(cls):
        return 'Auto'

    def get_state(self, current_temp):
        def do(session):
            system_settings = system.get_current_system_settings(session)
            program = system_settings.current_program

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
