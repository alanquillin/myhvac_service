from myhvac_service import db
from flask_restful import Resource

import logging

LOG = logging.getLogger(__name__)


class BaseResource(Resource):
    @staticmethod
    def sessionize(func, *args, **kwargs):
        session = db.Session()
        ret = None
        try:
            ret = func(session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return ret

    @staticmethod
    def get_sensor_id(session, sensor_id):
        try:
            sensor_id = int(sensor_id)
            sensor_id = db.get_sensor_id(session, id=sensor_id)

            if not sensor_id:
                LOG.debug('Could not retrieve sensor_id \'%s\' via the id field, '
                          'trying the manufacturer id', sensor_id)
                sensor_id = db.get_sensor_id(session, manufacturer_id=sensor_id)

            return sensor_id
        except ValueError:
            return db.get_sensor_id(session, manufacturer_id=sensor_id)

    @staticmethod
    def get_sensor(session, sensor_id):
        try:
            sensor_id = int(sensor_id)
            sensor = db.get_sensor_by_id(session, sensor_id)

            if not sensor:
                LOG.debug('Could not retrieve sensor_id \'%s\' via the id field, '
                          'trying the manufacturer id', sensor_id)
                sensor = db.get_sensor(session, manufacturer_id=sensor_id)

            return sensor
        except ValueError:
            return db.get_sensor(session, manufacturer_id=sensor_id)