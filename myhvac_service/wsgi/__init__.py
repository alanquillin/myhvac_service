from flask import Flask
from flask_restful import Api
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from myhvac_core import cfg
from myhvac_service.wsgi import measurements
from myhvac_service.wsgi import sensors
from myhvac_service.wsgi import system

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.BoolOpt('debug', default=False,
                help='Enables debug mode for the flask rest api'),
    cfg.IntOpt('port', default=8080, help='Http port of the webserver')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'rest_api')


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


api.add_resource(sensors.Sensors, '/sensors')
api.add_resource(sensors.Sensor, '/sensors/<sensor_id>')
api.add_resource(measurements.SensorMeasurements, '/sensors/<sensor_id>/measurements')
api.add_resource(measurements.SensorTempuratures, '/sensors/<sensor_id>/measurements/temperatures')
api.add_resource(system.SystemState, '/system/state')
api.add_resource(system.SystemPing, '/system/ping')


def run():
    LOG.info('Starting web server...')
    LOG.debug('Enable flask debug: %s', CONF.rest_api.debug)
    LOG.debug('Enable port: %s', CONF.rest_api.port)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(CONF.rest_api.port)
    IOLoop.instance().start()


def stop():
    LOG.info('Stopping web server...')
    IOLoop.instance().stop()