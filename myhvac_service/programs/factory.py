from myhvac_core.db import api as db
from myhvac_core.db import system
from myhvac_service.programs.types.auto import AutoProgram
from myhvac_service.programs.types.manual import ManualProgram
from myhvac_service.programs.types.off import OffProgram

import logging

LOG = logging.getLogger(__name__)


def get_program():
    def do(session):
        system_config = system.get_current_system_config(session)

        program = system_config.current_program
        prog_type_name = program.program_type.name

        if prog_type_name == AutoProgram.get_program_type():
            return AutoProgram(program.name, program.id)

        if prog_type_name == ManualProgram.get_program_type():
            return ManualProgram(program.name, program.id)

        if prog_type_name != OffProgram.get_program_type():
            LOG.error('System set to unknown program type \'%s\'.  Defaulting to Off', prog_type_name)

        return OffProgram(program.name, program.id)

    return db.sessionize(do)
