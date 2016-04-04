from flask import Flask
from flask_restful import abort
from flask_restful import Api
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


class SensorTempuratures(Resource):
    def __init__(self):
        self._post_parser = reqparse.RequestParser()
        self._post_parser.add_argument('temp', required=True)
        self._post_parser.add_argument('sensor_id', required=True)

    @marshal_with(dict(temp=fields.Nested(dict())))
    def post(self, **kwargs):
        args = self._post_parser.parse_args()
        temp = args.get('temp')

        if not temp:
            abort(400, )

api.add_resource(SensorTempuratures, '/sensors/<sensor_id>/temperatures/')
