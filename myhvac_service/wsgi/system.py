from myhvac_service import hvac
from myhvac_service import system_state as states
from myhvac_service import temp
from myhvac_service.system_modes import factory as prog_factory
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class SystemState(BaseResource):
    def get(self):
        rs, es = hvac.get_system_state()
        curr_temp = temp.get_current_temp()
        # program = prog_factory.get_program()
        # prog_setting = program.get_current_setting()

        data = dict(state=states.print_state(rs),
                    current_temp=curr_temp)
        # data = dict(state=states.print_state(rs),
        #             current_temp=curr_temp,
        #             program=dict(name=program.name,
        #                          id=program.id,
        #                          current_setting=prog_setting))

        if rs != es:
            data['error'] = True
            data['error_message'] = 'Current system state \'%s\' does not match expected system state \'%s\'' % \
                                    (states.print_state(rs), states.print_state(es))

        return data


class SystemPing(BaseResource):
    def get(self):
        return 'pong'