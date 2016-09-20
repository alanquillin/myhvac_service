from myhvac_service.db import models


def _get_sensors(session, **kwargs):
    return session.query(models.Sensor).filter_by(**kwargs)


def get_sensors(session, **kwargs):
    return _get_sensors(session, **kwargs).all()


def get_sensor_by_id(session, id):
    return session.query(models.Sensor).get(id)


def get_sensor(session, **kwargs):
    return _get_sensors(session, **kwargs).one_or_none()


def get_sensor_id(session, **kwargs):
    return _get_sensors(session, **kwargs).add_column(models.Sensor.id).one_or_none()


def sensor_exists(session, **kwargs):
    return get_sensor(session, **kwargs).exists()


def insert_sensor(session, name, manufacturer_id, model, manufacturer):
    sensor_type = get_sensor_types(session, model=model, manufacturer=manufacturer)\
        .add_column(models.SensorType.id).one_or_none()
    if not sensor_type:
        sensor_type = models.SensorType(model=model, manufacturer=manufacturer)
        session.add(sensor_type)
        session.commit()
    sensor = models.Sensor(name=name, manufacturer_id=manufacturer_id, sensor_type_id=sensor_type.id)
    session.add(sensor)
    return sensor


def get_sensor_types(session, **kwargs):
    return session.query(models.SensorType).filter_by(**kwargs)
