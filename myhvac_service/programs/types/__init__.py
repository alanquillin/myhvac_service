from myhvac_core import system_state as states

import logging
import sys

LOG = logging.getLogger(__name__)


class BaseProgramType(object):
    def __init__(self, name, id_):
        self._name = name
        self._id = id_
        pass

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @staticmethod
    def _get_state(current_temp, program_setting):
        cool_threshold = program_setting.cool_threshold
        heat_threshold = program_setting.heat_threshold
        fan_on = program_setting.fan_on

        if cool_threshold <= 0:
            cool_threshold = sys.maxint

        LOG.debug('Determining system state.  Current temp: %s, Cool threshold: %s, Heat threshold: %s, Fan On: %s',
                  current_temp, cool_threshold, heat_threshold, fan_on)

        if current_temp > cool_threshold:
            return states.COOL

        if current_temp < heat_threshold:
            return states.HEAT

        if fan_on:
            return states.FAN_ONLY

        return states.OFF

    @staticmethod
    def _parse_program_settings(setting):
        return dict(id=setting.id,
                    cool_threshold=setting.cool_threshold,
                    heat_threshold=setting.heat_threshold,
                    fan_on=setting.fan_on)