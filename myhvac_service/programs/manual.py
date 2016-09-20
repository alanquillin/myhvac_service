from myhvac_service import db
from myhvac_service.db import system
from myhvac_service.programs import ProgramBase

import logging

LOG = logging.getLogger(__name__)


class ManualProgram(ProgramBase):
    def __init__(self, id_):
        super(ManualProgram, self).__init__(id_)

    @classmethod
    def name(cls):
        return 'Manual'

    def get_state(self, current_temp):
        def do(session):
            system_settings = system.get_current_system_settings(session)
            return self._get_state(current_temp, system_settings.manual_cool_temp, system_settings.manual_heat_temp)

        return db.sessionize(do)