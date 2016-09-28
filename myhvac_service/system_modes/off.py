from myhvac_service import system_state as states
from myhvac_service.system_modes import SystemModeBase

import logging

LOG = logging.getLogger(__name__)


class OffMode(SystemModeBase):
    def __init__(self, id_):
        super(OffMode, self).__init__(id_)

    @classmethod
    def name(cls):
        return 'Off'

    def get_state(self, *_):
        return states.OFF

    def program_name(self):
        return self.name()
