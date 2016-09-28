from myhvac_service import hvac
from myhvac_service import system_state as states
from myhvac_service import temp
from myhvac_service.system_modes import factory as sys_mode_factory
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class SystemState(BaseResource):
    def get(self):
        rs, es = hvac.get_system_state()
        curr_temp = temp.get_current_temp()
        mode = sys_mode_factory.get_system_mode()

        data = dict(system_state=states.print_state(rs),
                    expected_program_state=states.print_state(mode.get_state(curr_temp)),
                    current_temp=curr_temp,
                    system_mode=mode.to_dict())

        if rs != es:
            data['error'] = True
            data['error_message'] = 'Current system state \'%s\' does not match expected system state \'%s\'' % \
                                    (states.print_state(rs), states.print_state(es))

        return data


class SystemPing(BaseResource):
    def get(self):
        return 'pong'