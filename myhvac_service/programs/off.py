from myhvac_service import system_state as states
from myhvac_service.programs import ProgramBase

import logging

LOG = logging.getLogger(__name__)


class OffProgram(ProgramBase):
    def __init__(self, id_):
        super(OffProgram, self).__init__(id_)

    @classmethod
    def name(cls):
        return 'Off'

    def get_state(self, *_):
        return states.OFF
