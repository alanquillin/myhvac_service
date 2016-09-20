from myhvac_service.db import models

import logging

LOG = logging.getLogger(__name__)


def get_current_system_settings(session):
    return session.query(models.SystemSettings)\
        .filter_by(active=True)\
        .order_by(models.SystemSettings.created_at.desc())\
        .first()
