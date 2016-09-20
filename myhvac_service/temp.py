from myhvac_service import cfg
from myhvac_service import db
from myhvac_service.db import models

import logging
from datetime import datetime, timedelta

opts = [
    cfg.IntOpt('max_measurement_age_threshold_min', default=12,
               help='The maximum age (in minutes) of the most recent temperature measurement for a '
                    'sensor to be considered when calculating overall system temperature')
]

CONF = cfg.CONF
CONF.register_opts(opts, 'temp')

LOG = logging.getLogger(__name__)


def get_current_temp():
    def do(session):
        temp_agg = 0
        temp_cnt = 0

        room_models = db.get_rooms(session)

        LOG.debug(room_models)
        for room_model in room_models:
            LOG.debug(room_model)
            if not room_model.active:
                continue

            room_temp = None
            measurement_agg = 0
            measurement_cnt = 0

            if room_model.sensors:
                for sensor_model in room_model.sensors:
                    LOG.debug(sensor_model)
                    measurement = db.get_most_recent_sensor_temperature(session,
                                                                        sensor_id=sensor_model.id,
                                                                        order_desc=True,
                                                                        order_by=models.Measurement.recorded_date)
                    delta_min = CONF.temp.max_measurement_age_threshold_min
                    if measurement and measurement.recorded_date > datetime.now() - timedelta(minutes=delta_min):
                        measurement_agg = measurement.measurement
                        measurement_cnt = measurement_cnt + 1

            if measurement_cnt > 0 and measurement_agg > 0:
                room_temp = measurement_agg / measurement_cnt

            if room_temp:
                temp_agg = temp_agg + (room_temp * room_model.weight)
                temp_cnt = temp_cnt + room_model.weight

        if not temp_cnt and not temp_agg:
            LOG.warn('No temperature data available.  Either no data exists, or the data that exists is too old.')
            return None

        return temp_agg / temp_cnt

    return db.sessionize(do)
