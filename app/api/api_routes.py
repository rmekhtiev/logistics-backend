from app.api.api_classes import *

from app.api import api


api.add_resource(HelloWorld, '/api/v1.0/hello')


""" Applications """

api.add_resource(Applications, '/api/v1.0/applications')
api.add_resource(ApplicationSingle, '/api/v1.0/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/api/v1.0/applications/<application_id>/cargos')
api.add_resource(ApplicationsDrivers, '/api/v1.0/applications/<application_id>/drivers')
api.add_resource(ApplicationsCars, '/api/v1.0/applications/<application_id>/cars')


""" Drivers """

api.add_resource(Drivers, '/api/v1.0/drivers')
api.add_resource(DriverSingle, '/api/v1.0/drivers/<driver_id>')
api.add_resource(DriversService, '/api/v1.0/drivers/<driver_id>/service')
api.add_resource(DriversApplications, '/api/v1.0/drivers/<driver_id>/applications')

""" Cars """

api.add_resource(Cars, '/api/v1.0/cars')
api.add_resource(CarSingle, '/api/v1.0/cars/<car_id>')
api.add_resource(CarsService, '/api/v1.0/cars/<car_id>/service')
api.add_resource(CarsApplications, '/api/v1.0/cars/<car_id>/applications')

""" Clients """

api.add_resource(Clients, '/api/v1.0/clients')
api.add_resource(ClientSingle, '/api/v1.0/clients/<client_id>')
api.add_resource(ClientContracts, '/api/v1.0/clients/<client_id>/contracts')


""" Contracts """

api.add_resource(Contracts, '/api/v1.0/contracts')
api.add_resource(ContractSingle, '/api/v1.0/contracts/<contract_id>')
api.add_resource(ContractApp, '/api/v1.0/contracts/<contract_id>/app')
api.add_resource(ContractClient, '/api/v1.0/contracts/<contract_id>/client')


""" Requisites """

api.add_resource(Requisites, '/api/v1.0/requisites')
api.add_resource(RequisiteSingle, '/api/v1.0/requisites/<requisite_id>')


""" Contacts """

api.add_resource(Contacts, '/api/v1.0/contacts')
api.add_resource(ContactSingle, '/api/v1.0/contacts/<contact_id>')
api.add_resource(ContactApp, '/api/v1.0/contacts/<contact_id>/app')


""" Cargos """

api.add_resource(Cargos, '/api/v1.0/cargos')
api.add_resource(CargoSingle, '/api/v1.0/cargos/<cargo_id>')
api.add_resource(CargoApp, '/api/v1.0/cargos/<cargo_id>/app')
