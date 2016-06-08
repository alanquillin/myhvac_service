from myhvac_core import system_state as states
from myhvac_service.programs.types import BaseProgramType

import logging

LOG = logging.getLogger(__name__)


class OffProgram(BaseProgramType):
    def __init__(self, name, id_):
        super(OffProgram, self).__init__(name, id_)

    @classmethod
    def get_program_type(cls):
        return 'off'

    def get_state(self, *_):
        return states.OFF
