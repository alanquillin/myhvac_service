from myhvac_core import hvac
from myhvac_core import system_state as states
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class SystemState(BaseResource):
    def get(self):
        state = hvac.get_system_state()
        return dict(state=states.print_state(state))

    def post(self):
        pass


class SystemPing(BaseResource):
    def get(self):
        return 'pong'