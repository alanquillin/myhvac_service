from myhvac_core import hvac
from myhvac_service.display import api as display
from myhvac_service import hub
from myhvac_service import prog_manager as pm

def main():
    display.write('Starting up system...')
    hvac.init_gpio()

    prog_man = pm.ProgramManager()

    try:
        hub.joinall(hub.spawn(prog_man.start))
    finally:
        prog_man.close()
