from flask_restful import abort
from flask_restful import reqparse

from myhvac_service import db
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class SensorResource(BaseResource):
    @staticmethod
    def parse_sensor(sensor):
        LOG.debug('Parsing data: %s', sensor)
        if not sensor:
            return None
        s = dict(id=sensor.id,
                 name=sensor.name,
                 manufacturer_id=sensor.manufacturer_id)
        if sensor.sensor_type:
            s['type'] = dict(id=sensor.sensor_type.id,
                             model=sensor.sensor_type.model,
                             manufacturer=sensor.sensor_type.manufacturer)

        LOG.debug('Parsed data: %s %s', type(s), s)
        return s


class Sensors(SensorResource):
    def get(self, **kwargs):
        def do(session, *args, **kwargs):
            sensors = db.get_sensors(session)
            sensors_d = []
            for sensor in sensors:
                sensors_d.append(self.parse_sensor(sensor))
            return sensors

        sensors = self.sessionize(do, **kwargs)

        return dict(sensors=sensors)

    def post(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('sensor', type=dict, required=True, location='json')

        def do(session, *args, **kwargs):
            args = parser.parse_args()
            LOG.debug("args: %s" % args)
            sensor = args.get('sensor')
            LOG.debug('sensor %s: %s' % (type(sensor), sensor))
            sensor_type = sensor.get('type')
            LOG.debug('type %s: %s' % (type(sensor_type), sensor_type))

            sensor = db.insert_sensor(session, sensor['name'], sensor['manufacturer_id'],
                                      sensor_type['model'], sensor_type['manufacturer'])

            return self.parse_sensor(sensor)

        sensor = self.sessionize(do, **kwargs)

        return sensor, 201


class Sensor(SensorResource):
    def get(self, sensor_id, **kwargs):
        LOG.debug('Retrieving sensors %s...', sensor_id)

        def do(session, sensor_id, *args, **kwargs):
            sensor = self.get_sensor(session, sensor_id)
            if not sensor:
                return None
            return self.parse_sensor(sensor)

        sensor = self.sessionize(do, sensor_id, **kwargs)

        if not sensor:
            abort(404)

        return dict(sensor=sensor)