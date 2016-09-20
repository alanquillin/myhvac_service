from myhvac_service import system_state as states

import logging
import sys

LOG = logging.getLogger(__name__)


class ProgramBase(object):
    def __init__(self, id_):
        self._id = id_
        pass

    @property
    def id(self):
        return self._id

    @staticmethod
    def _get_state(current_temp, cool_temp, heat_temp):

        if cool_temp <= 0:
            cool_temp = sys.maxint

        LOG.debug('Determining system state.  Current temp: %s, Cool threshold: %s, Heat threshold: %s',
                  current_temp, cool_temp, heat_temp)

        if current_temp > cool_temp:
            return states.COOL

        if current_temp < heat_temp:
            return states.HEAT

        return states.OFF

    @staticmethod
    def _parse_program_settings(setting):
        return dict(id=setting.id,
                    cool_threshold=setting.cool_temp,
                    heat_threshold=setting.heat_temp)