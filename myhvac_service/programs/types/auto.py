from myhvac_core.db import api as db
from myhvac_core.db import programs
from myhvac_core.db import system
from myhvac_core import system_state as states
from myhvac_service.programs.types import BaseProgramType

import logging

LOG = logging.getLogger(__name__)


class AutoProgram(BaseProgramType):
    def __init__(self, name, id_):
        super(AutoProgram, self).__init__(name, id_)

    @classmethod
    def get_program_type(cls):
        return 'auto'

    def get_state(self, current_temp):
        def do(session):
            system_config = system.get_current_system_config(session)
            program_id = system_config.current_program_id
            program_name = system_config.current_program.name
            program_settings = programs.get_active_program_settings_by_program(session,
                                                                               program_id=program_id)

            if not program_settings:
                LOG.error('No active program settings found for program \'%s\'.  Setting system to off', program_name)
                return states.OFF

            return self._get_state(current_temp, program_settings[0])

        return db.sessionize(do)
