from flask_restful import Resource

from app.api.api_classes import *

from app.api import api


api.add_resource(HelloWorld, '/api/v1.0/hello')

""" Applications """
api.add_resource(ApplicationsList, '/api/v1.0/applications')
api.add_resource(ApplicationSingle, '/api/v1.0/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/api/v1.0/applications/<application_id>/cargos')

""" Drivers """
api.add_resource(Drivers, '/api/v1.0/drivers')
api.add_resource(DriverSingle, '/api/v1.0/drivers/<driver_id>')
# api.add_resource(DriversService, '/api/v1.0/drivers/<driver_id>/service') TODO: create Drivers service (apps done)
""" Cars """
api.add_resource(Cars, '/api/v1.0/cars')
