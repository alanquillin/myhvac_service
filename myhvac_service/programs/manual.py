from myhvac_core import system_state as states


class ManualProgram(object):
    def __init__(self):
        pass

    def get_state(self, current_temp):
        if current_temp > 70:
            return states.COOL

        return states.OFF
