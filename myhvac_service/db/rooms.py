from myhvac_service.db import models

from sqlalchemy import func

from datetime import datetime


def _get_rooms(session, **kwargs):
    return session.query(models.Room).filter_by(**kwargs)


def get_rooms(session, **kwargs):
    return _get_rooms(session, **kwargs).all()


def get_room_by_id(session, id):
    return session.query(models.Room).get(id)


def get_rooms_dashboard(session, **kwargs):
    return _get_rooms(session, **kwargs)
