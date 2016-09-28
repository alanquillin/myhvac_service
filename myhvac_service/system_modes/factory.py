from myhvac_service import db
from myhvac_service.db import system
from myhvac_service.system_modes.auto import AutoMode
from myhvac_service.system_modes.manual import ManualMode
from myhvac_service.system_modes.off import OffMode

import logging

LOG = logging.getLogger(__name__)


def get_system_mode():
    def do(session):
        system_settings = system.get_current_system_settings(session)

        mode = system_settings.system_mode

        if mode.name == AutoMode.name():
            return AutoMode(mode.id, system_settings.current_program)

        if mode.name == ManualMode.name():
            return ManualMode(mode.id)

        if mode.name != OffMode.name():
            LOG.error('System set to unknown mode \'%s\'.  Defaulting to Off', mode.name)

        return OffMode(mode.id)

    return db.sessionize(do)
