from flask_restful import Resource

from app.api.api_classes import *

from app.api import api


api.add_resource(HelloWorld, '/api/v1.0/hello')

api.add_resource(ApplicationsList, '/api/v1.0/applications')
api.add_resource(ApplicationSingle, '/api/v1.0/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/api/v1.0/applications/<application_id>/cargos')
