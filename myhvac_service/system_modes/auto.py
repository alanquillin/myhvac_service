from myhvac_service import db
from myhvac_service.db import system
from myhvac_service import system_state as states
from myhvac_service.system_modes import SystemModeBase
from myhvac_service import utils

import logging

LOG = logging.getLogger(__name__)


class AutoMode(SystemModeBase):
    def __init__(self, id_, program):
        super(AutoMode, self).__init__(id_)
        self._set_program_name(program)

    @classmethod
    def name(cls):
        return 'Auto'

    def get_state(self, current_temp):
        def do(session):
            system_settings = system.get_current_system_settings(session)
            program = system_settings.current_program

            self._set_program_name(program)

            if not program:
                LOG.warn('No program set for system.')
                return states.OFF
            elif not program.schedules:
                LOG.warn('No schedules found for program \'%s\'.  Setting system to Off', program.name)
                return states.OFF

            schedule = utils.get_active_schedule(program)
            if not schedule:
                LOG.error('Could not determine the ')
            return self._get_state(current_temp, schedule.cool_temp, schedule.heat_temp)

        return db.sessionize(do)

    def program_name(self):
        return "%s (%s)" % (self._program_name, self.name())

    def to_dict(self):
        def do(session):
            system_settings = system.get_current_system_settings(session)
            program = system_settings.current_program
            program_data = None

            if program:
                program_data = dict(name=program.name)
                schedule, next_schedule = utils.get_active_and_next_schedule(program)

                schedule_data = self._build_schedule_dict(schedule)
                next_schedule_data = self._build_schedule_dict(next_schedule)

                program_data['active_schedule'] = schedule_data
                program_data['next_schedule'] = next_schedule_data

            return dict(name=self.name(), program=program_data)

        return db.sessionize(do)

    def _build_schedule_dict(self, schedule):
        if not schedule:
            return None

        return dict(days_of_week=schedule.days_of_week(),
                    time_of_day=str(schedule.time_of_day),
                    cool_temp=schedule.cool_temp,
                    heat_temp=schedule.heat_temp)

    def _set_program_name(self, program):
        self._program_name = 'Unknown'

        if program:
            self._program_name = program.name
