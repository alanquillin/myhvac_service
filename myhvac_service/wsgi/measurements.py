from flask_restful import abort
from flask_restful import reqparse

from myhvac_service import db
from myhvac_service.wsgi.base import BaseResource

import logging

LOG = logging.getLogger(__name__)


class MeasurementResource(BaseResource):
    @staticmethod
    def parse_temp(temp):
        if not temp:
            return None
        return dict(id=temp.id,
                    measurement=temp.measurement,
                    recorded_date=temp.recorded_date.isoformat())


class SensorTempuratures(MeasurementResource):
    def post(self, sensor_id, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('temperature', type=dict, required=True, location='json')

        def do(session, sensor_id, *args, **kwargs):
            args = parser.parse_args()
            temp = args.get('temperature')

            sensor = self.get_sensor(session, sensor_id)

            if not sensor:
                LOG.debug('Cold not find sensor with id: %s', sensor_id)
                abort(404)

            temp  = db.insert_sensor_temperature(session, sensor.id, temp.get('f'))
            return self.parse_temp(temp)

        temp = self.sessionize(do, sensor_id, **kwargs)

        return temp, 201


class SensorMeasurements(MeasurementResource):
    def post(self, sensor_id, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('measurement', type=dict, required=True, location='json')

        def do(session, sensor_id, *args, **kwargs):
            args = parser.parse_args()
            measurement = args.get('measurement')

            sensor = self.get_sensor(session, sensor_id)

            if not sensor:
                abort(404)

            type = measurement.get('type')
            temp = db.insert_sensor_measurement(session, sensor.id, type, measurement.get('data'))

            return self.parse_temp(temp)

        temp = self.sessionize(do, sensor_id, **kwargs)

        return temp, 201
