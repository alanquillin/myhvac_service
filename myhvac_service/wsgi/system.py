from myhvac_core import hvac
from myhvac_core import system_state as states
from myhvac_core import temp
from myhvac_service.programs import factory as prog_factory
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class SystemState(BaseResource):
    def get(self):
        rs, es = hvac.get_system_state()
        curr_temp = temp.get_current_temp()
        program = prog_factory.get_program()

        data = dict(state=states.print_state(rs),
                    current_temp=curr_temp,
                    program=program.name)

        if rs != es:
            data['error'] = True
            data['error_message'] = 'Current system state \'%s\' does not match expected system state \'%s\'' % \
                                    (states.print_state(rs), states.print_state(es))

        return data


class SystemPing(BaseResource):
    def get(self):
        return 'pong'