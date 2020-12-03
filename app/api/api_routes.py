from app.api.api_classes import *

from app.api import api


api.add_resource(HelloWorld, '/api/v2.0/hello')


""" Applications """

api.add_resource(Applications, '/api/v2.0/applications')
api.add_resource(ApplicationSingle, '/api/v2.0/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/api/v2.0/applications/<application_id>/cargos')
api.add_resource(ApplicationSingleDrivers, '/api/v2.0/applications/<application_id>/drivers')
api.add_resource(ApplicationSingleCars, '/api/v2.0/applications/<application_id>/cars')
api.add_resource(ApplicationSingleDriverSingle, '/api/v2.0/applications/<application_id>/drivers/<driver_id>')
api.add_resource(ApplicationSingleCarSingle, '/api/v2.0/applications/<application_id>/cars/<car_id>')


""" Drivers """

api.add_resource(Drivers, '/api/v2.0/drivers')
api.add_resource(DriverSingle, '/api/v2.0/drivers/<driver_id>')
api.add_resource(DriversService, '/api/v2.0/drivers/<driver_id>/service')
api.add_resource(DriversApplications, '/api/v2.0/drivers/<driver_id>/applications')

""" Cars """

api.add_resource(Cars, '/api/v2.0/cars')
api.add_resource(CarSingle, '/api/v2.0/cars/<car_id>')
api.add_resource(CarsService, '/api/v2.0/cars/<car_id>/service')
api.add_resource(CarsApplications, '/api/v2.0/cars/<car_id>/applications')

""" Clients """

api.add_resource(Clients, '/api/v2.0/clients')
api.add_resource(ClientSingle, '/api/v2.0/clients/<client_id>')
api.add_resource(ClientContracts, '/api/v2.0/clients/<client_id>/contracts')


""" Contracts """

api.add_resource(Contracts, '/api/v2.0/contracts')
api.add_resource(ContractSingle, '/api/v2.0/contracts/<contract_id>')
api.add_resource(ContractApp, '/api/v2.0/contracts/<contract_id>/app')
api.add_resource(ContractClient, '/api/v2.0/contracts/<contract_id>/client')


""" Requisites """

api.add_resource(Requisites, '/api/v2.0/requisites')
api.add_resource(RequisiteSingle, '/api/v2.0/requisites/<requisite_id>')


""" Contacts """

api.add_resource(Contacts, '/api/v2.0/contacts')
api.add_resource(ContactSingle, '/api/v2.0/contacts/<contact_id>')
api.add_resource(ContactApp, '/api/v2.0/contacts/<contact_id>/app')


""" Cargos """

api.add_resource(Cargos, '/api/v2.0/cargos')
api.add_resource(CargoSingle, '/api/v2.0/cargos/<cargo_id>')
api.add_resource(CargoApp, '/api/v2.0/cargos/<cargo_id>/app')


""" Routes """

api.add_resource(Routes, '/api/v2.0/routes')
api.add_resource(RouteSingle, '/api/v2.0/routes/<route_id>')
