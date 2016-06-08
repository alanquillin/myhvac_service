from myhvac_core.db import api as db
from myhvac_core.db import programs
from myhvac_core import system_state as states
from myhvac_service.programs.types import BaseProgramType

import logging

LOG = logging.getLogger(__name__)


class ManualProgram(BaseProgramType):
    def __init__(self, name, id_):
        super(ManualProgram, self).__init__(name, id_)

    @classmethod
    def get_program_type(cls):
        return 'manual'

    def get_state(self, current_temp):
        def do(session):
            program_settings = programs.get_active_program_settings_by_program(session, program_id=self.id)

            if not program_settings:
                LOG.error('No active manual program settings found.  Setting system to off')
                return states.OFF

            return self._get_state(current_temp, program_settings[0])

        return db.sessionize(do)
