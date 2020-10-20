from app.api.api_classes import *

from app.api import api


api.add_resource(HelloWorld, '/api/v1.0/hello')

""" Applications """
api.add_resource(Applications, '/api/v1.0/applications')
api.add_resource(ApplicationSingle, '/api/v1.0/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/api/v1.0/applications/<application_id>/cargos')

""" Drivers """
api.add_resource(Drivers, '/api/v1.0/drivers')
api.add_resource(DriverSingle, '/api/v1.0/drivers/<driver_id>')
# api.add_resource(DriversService, '/api/v1.0/drivers/<driver_id>/service') TODO: create Drivers service (apps done)

""" Cars """
api.add_resource(Cars, '/api/v1.0/cars')
api.add_resource(CarSingle, '/api/v1.0/cars/<car_id>')
# api.add_resource(DriversService, '/api/v1.0/drivers/<driver_id>/service') TODO: create Cars service (apps travelled)

""" Clients """
api.add_resource(Clients, '/api/v1.0/clients')
api.add_resource(ClientSingle, '/api/v1.0/clients/<client_id>')
api.add_resource(ClientContracts, '/api/v1.0/clients/<client_id>/contracts')

""" Contracts """
api.add_resource(Contracts, '/api/v1.0/contracts')
api.add_resource(ContractSingle, '/api/v1.0/contracts/<contract_id>')