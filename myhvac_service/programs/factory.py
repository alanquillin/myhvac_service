from myhvac_service.programs.auto import AutoProgram
from myhvac_service.programs.manual import ManualProgram

programs = dict(auto=AutoProgram(), manual=ManualProgram())


def get_program():
    return programs['manual']
