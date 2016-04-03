from myhvac_service.display.drivers import factory

import logging

LOG = logging.getLogger(__name__)

driver = factory.get_driver()


def write(msg):
    driver.write(msg)


def update(**kwargs):
    driver.write('this is the default')
