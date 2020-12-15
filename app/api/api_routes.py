from app.api import api
from app.api.api_classes import *


""" Applications """

api.add_resource(Applications, '/applications')
api.add_resource(ApplicationSingle, '/applications/<application_id>')
api.add_resource(ApplicationSingleCargos, '/applications/<application_id>/cargos')
api.add_resource(ApplicationSingleDrivers, '/applications/<application_id>/drivers')
api.add_resource(ApplicationSingleCars, '/applications/<application_id>/cars')
api.add_resource(ApplicationSingleDriverSingle, '/applications/<application_id>/drivers/<driver_id>')
api.add_resource(ApplicationSingleCarSingle, '/applications/<application_id>/cars/<car_id>')


""" Drivers """

api.add_resource(Drivers, '/drivers')
api.add_resource(DriverSingle, '/drivers/<driver_id>')
api.add_resource(DriversService, '/drivers/<driver_id>/service')
api.add_resource(DriversApplications, '/drivers/<driver_id>/applications')

""" Cars """

api.add_resource(Cars, '/cars')
api.add_resource(CarSingle, '/cars/<car_id>')
api.add_resource(CarsService, '/cars/<car_id>/service')
api.add_resource(CarsApplications, '/cars/<car_id>/applications')

""" Clients """

api.add_resource(Clients, '/clients')
api.add_resource(ClientSingle, '/clients/<client_id>')
api.add_resource(ClientContracts, '/clients/<client_id>/contracts')


""" Contracts """

api.add_resource(Contracts, '/contracts')
api.add_resource(ContractSingle, '/contracts/<contract_id>')
api.add_resource(ContractApp, '/contracts/<contract_id>/app')
api.add_resource(ContractClient, '/contracts/<contract_id>/client')


""" Requisites """

api.add_resource(Requisites, '/requisites')
api.add_resource(RequisiteSingle, '/requisites/<requisite_id>')


""" Contacts """

api.add_resource(Contacts, '/contacts')
api.add_resource(ContactSingle, '/contacts/<contact_id>')
api.add_resource(ContactApp, '/contacts/<contact_id>/app')


""" Cargos """

api.add_resource(Cargos, '/cargos')
api.add_resource(CargoSingle, '/cargos/<cargo_id>')
api.add_resource(CargoApp, '/cargos/<cargo_id>/app')


""" Routes """

api.add_resource(Routes, '/routes')
api.add_resource(RouteSingle, '/routes/<route_id>')
