from myhvac_service import db
from myhvac_service.db import system
from myhvac_service.programs.auto import AutoProgram
from myhvac_service.programs.manual import ManualProgram
from myhvac_service.programs.off import OffProgram

import logging

LOG = logging.getLogger(__name__)


def get_program():
    def do(session):
        system_config = system.get_current_system_settings(session)

        program = system_config.current_program

        if program.name == AutoProgram.name():
            return AutoProgram(program.name, program.id)

        if program.name == ManualProgram.name():
            return ManualProgram(program.name, program.id)

        if program.name != OffProgram.name():
            LOG.error('System set to unknown program type \'%s\'.  Defaulting to Off', program.name)

        return OffProgram(program.name, program.id)

    return db.sessionize(do)
