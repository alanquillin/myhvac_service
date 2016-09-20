OFF = 0
HEAT = 1
COOL = 2
FAN_ONLY = 3
UNKNOWN = -1

_states = {HEAT: "Heat", COOL: "Cool", FAN_ONLY: 'Fan Only', OFF: 'Off', UNKNOWN: 'Unknown'}


def print_state(state):
    return _states.get(state, _states[UNKNOWN])


def system_state_from_str(str):
    for k, v in _states.iteritems():
        if str.lower() == v.lower():
            return k

    return UNKNOWN
