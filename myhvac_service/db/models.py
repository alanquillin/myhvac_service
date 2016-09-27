import logging

from myhvac_service import utils

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, DateTime, Boolean, Table, Float, Time
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

LOG = logging.getLogger(__name__)


Base = declarative_base()


class ParseableModel(object):
    def to_dict(self):
        return self.__dict__

    def to_dict2(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d


class SensorType(Base):
    __tablename__ = 'sensor_types'
    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)

    def __str__(self):
        return '%s <id:%s, model:%s, manufacturer:%s>' % (self.__class__.__name__,
                                                          self.id, self.model, self.manufacturer)


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manufacturer_id = Column(String(255), nullable=True)
    sensor_type_id = Column(Integer, ForeignKey('sensor_types.id'), nullable=True)
    sensor_type = relationship(SensorType)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=True)

    def __str__(self):
        return '%s <id:%s, name:%s, manufacturer_id:%s, room_id:%s, sensor_type_id:%s>' % \
               (self.__class__.__name__, self.id, self.name,
                self.manufacturer_id, self.room_id, self.sensor_type_id)


class MeasurementType(Base):
    __tablename__ = 'measurement_types'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(15), nullable=False)

    def __str__(self):
        return '%s <id:%s, name:%s>' % (self.__class__.__name__, self.id, self.name)


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(BigInteger, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    measurement_type_id = Column(Integer, ForeignKey('measurement_types.id'), nullable=False)
    data = Column(Float, nullable=False)
    recorded_date = Column(DateTime, nullable=False)
    measurement_type = relationship(MeasurementType)

    def __str__(self):
        return '%s <id:%s, sensor_id:%s, manufacturer_type_id:%s, data:%s, recorded_date:%s>' % \
               (self.__class__.__name__, self.id, self.sensor_id,
                self.manufacturer_type_id, self.data, self.recorded_date)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, nullable=False)
    weight = Column(Float, nullable=False)
    sensors = relationship(Sensor)

    def __str__(self):
        return '%s <id:%s, name:%s, active:%s, weight:%s>' % (self.__class__.__name__, self.id,
                                                              self.name, self.active, self.weight)


class ProgramSchedule(Base):
    __tablename__ = 'program_schedules'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    days_of_week_bin_aggr = Column(Integer, nullable=False)
    time_of_day = Column(Time, nullable=False)
    cool_temp = Column(Integer, nullable=False)
    heat_temp = Column(Integer, nullable=False)

    def __str__(self):
        return '%s <id:%s, program_id:%s, time_of_day:%s, cool_temp:%s, ' \
               'heat_temp:%s, days_of_week_bin_aggr=%s, days_of_week=%s>' % \
               (self.__class__.__name__, self.id, self.program_id, self.time_of_day, self.cool_temp,
                self.heat_temp, self.days_of_week_bin_aggr, self.days_of_week())

    def days_of_week(self):
        return utils.days_of_week_from_bin_aggr(self.days_of_week_bin_aggr)


class Program(Base, ParseableModel):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    schedules = relationship(ProgramSchedule)

    def __str__(self):
        return '%s <id:%s, name:%s>' % (self.__class__.__name__, self.id, self.name)


class SystemMode(Base):
    __tablename__ = 'system_modes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    has_programs = Column(Boolean, nullable=False)

    def __str__(self):
        return '%s <id:%s, name:%s>' % (self.__class__.__name__, self.id, self.name)


class SystemSettings(Base):
    __tablename__ = 'system_settings'
    id = Column(Integer, primary_key=True)
    current_program_id = Column(Integer, ForeignKey('programs.id'))
    current_program = relationship(Program)
    system_mode_id = Column(Integer, ForeignKey('system_modes.id'), nullable=False)
    system_mode = relationship(SystemMode)
    manual_cool_temp = Column(Float)
    manual_heat_temp = Column(Float)
    temporary_cool_temp = Column(Float)
    temporary_heat_temp = Column(Float)
    active = Column(BIT, nullable=False)

    def __str__(self):
        return '%s <id:%s, current_program_id=%s, system_mode_id=%s, manual_cool_temp=%s, ' \
               'manual_heat_temp=%s, temporary_cool_temp=%s, temporary_heat_temp=%s>' % \
               (self.__class__.__name__, self.id, self.current_program_id, self.system_mode_id,
                self.manual_cool_temp, self.manual_heat_temp, self.temporary_cool_temp, self.temporary_heat_temp)
