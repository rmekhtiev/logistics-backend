from flask import request
from flask_restful import Resource, reqparse
from app.models import *


class HelloWorld(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self):
        return {'Test message': 'Hello World'}

    # noinspection PyMethodMayBeStatic
    def post(self):
        json_in = request.get_json()
        return {'you sent': json_in}, 201


class Multi(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, num):
        return {'result': num * 10}


""" Клиенты (Clients) """


# Список всех клиентов
class Clients(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('passport_number', type=int, required=True,
                                 help='passport number not provided', location='json')
        self.parser.add_argument('passport_series', type=int, required=True,
                                 help='passport series not provided', location='json')
        self.parser.add_argument('last_name', type=str, required=True,
                                 help='last name not provided', location='json')
        self.parser.add_argument('first_name', type=str, required=True,
                                 help='first name not provided', location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('email', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=True,
                                 help='phone not provided', location='json')
        super(Clients, self).__init__()

    # Выдать список всех объектов Client
    # noinspection PyMethodMayBeStatic
    def get(self):
        clients_list = Client.query.all()
        data = Client.to_dict_list(clients_list)
        return {'data': data}, 200

    # Создать новый объект Client
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если клиент с такими паспортными данными уже существует
        if Client.query.filter_by(passport_number=data['passport_number'], passport_series=data['passport_series']).first(): # noqa
            return {'message': "Client with that passport data already exists"}, 409

        # Проверка на правильность телефонного номера
        if len(data['phone']) > 11 or data['phone'][0] != '7':
            return {'message': "Incorrect phone format"}, 409
        # Если клиент с таким телефоном уже есть
        if Client.query.filter_by(phone=data['phone']).first():
            return {'message': "Client with this phone already exists"}, 409

        client = Client()
        client.from_dict(data)
        db.session.add(client)
        db.session.commit()
        data = client.to_dict()
        return {'data': data}, 201


# Один клиент
class ClientSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('passport_number', type=int, required=False, location='json')
        self.parser.add_argument('passport_series', type=int, required=False, location='json')
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('email', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=False, location='json')
        super(ClientSingle, self).__init__()

    # Получить объект Client
    # noinspection PyMethodMayBeStatic
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        data = client.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Client
    # noinspection PyMethodMayBeStatic
    def put(self, client_id):
        client = Client.query.get_or_404(client_id)
        data = self.parser.parse_args()

        # Если клиент с такими паспортными данными уже существует
        if Client.query.filter_by(passport_number=data['passport_number'], passport_series=data['passport_series']).first(): # noqa
            return {'message': "Client with that passport data already exists"}, 409

        # Проверка на правильность телефонного номера
        if len(data['phone']) > 11 or data['phone'][0] != '7':
            return {'message': "incorrect phone format"}, 409

        # Если клиент с таким телефоном уже есть
        if Client.query.filter_by(phone=data['phone']).first():
            return {'message': "Client with this phone already exists"}, 409

        # Если клиент с таким e-mail уже есть
        if Client.query.filter_by(passport_number=data['email']).first():
            return {'message': "Client with this e-mail address already exists"}, 409

        # Если пытаются поменять клиенту номер паспорта, а такая комбинация уже есть у другого клиента
        if Client.query.filter_by(passport_number=data['passport_number'], passport_series=client.passport_series).first(): # noqa
            return {'message': "Client cannot have passport data that already exists (passport number bad)"}, 409

        # Если пытаются поменять клиенту серию паспорта, а такая комбинация уже есть у другого клиента
        if Client.query.filter_by(passport_number=client.passport_number, passport_series=data['passport_series']).first(): # noqa
            return {'message': "Client cannot have passport data that already exists (passport series bad)"}, 409

        client.from_dict(data)
        db.session.commit()
        return {'data': client.to_dict()}, 200

    # Удалить объект Client
    # noinspection PyMethodMayBeStatic
    def delete(self, client_id):
        client = Client.query.get_or_404(client_id)

        # Если хотят удалить клиента, у которого есть активные контракты
        client_contracts = client.contracts
        for contract in client_contracts:
            if contract.application.status == 'active':
                return {'message': "Cannot delete client with an active contract"}, 409

        db.session.delete(client)
        db.session.commit()
        data = client.to_dict()
        return {'data': data}, 200


# Список всех контрактов, которые заключал клиент с компанией
class ClientContracts(Resource):
    # Вывести список всех Contract у данного Client
    # noinspection PyMethodMayBeStatic
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        contracts = client.contracts
        return {'data': Contract.to_dict_list(contracts)}, 200


""" Контракты (Contract) """


# Список всех контрактов
class Contracts(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('conclusion_date', type=str, required=False,
                                 default=datetime.utcnow, location='json')
        self.parser.add_argument('cost', type=float, required=True,
                                 help='cost of the payment not provided', location='json')
        self.parser.add_argument('client_id', type=int, required=False, location='json')
        self.parser.add_argument('payment_type', type=str, required=False,
                                 default='банковский перевод', location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        self.parser.add_argument('requisite_id', type=int, required=False, location='json')

        super(Contracts, self).__init__()

    # Выдать список всех объектов типа Contract
    # noinspection PyMethodMayBeStatic
    def get(self):
        contracts_list = Contract.query.all()
        data = Contract.to_dict_list(contracts_list)
        return {'data': data}, 200

    # Добавить новый объект типа Contract
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если контракту присваивают application, который уже используется
        if data['application_id'] is not None:
            if Application.query.get_or_404(data['application_id']).contract:
                return {'message': "this application is already in use"}

        # На клиента проверку не делаем, так как он может иметь сколь угодно много контрактов

        # TODO: сделать проверку на корректность payment_type (в процессе понять какие возможные значения принимаются)

        contract = Contract()
        contract.from_dict(data)
        db.session.add(contract)
        db.session.commit()
        return {'data': contract.to_dict()}, 200


# Один контракт
class ContractSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('conclusion_date', type=str, required=False, location='json')
        self.parser.add_argument('cost', type=float, required=False, location='json')
        self.parser.add_argument('client_id', type=int, required=False, location='json')
        self.parser.add_argument('payment_type', type=str, required=False, location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        self.parser.add_argument('requisite_id', type=int, required=False, location='json')

        super(ContractSingle, self).__init__()

    # Получить объект Contract
    # noinspection PyMethodMayBeStatic
    def get(self, contract_id):
        contract = Contract.query.get_or_404(contract_id).to_dict()
        return {'data': contract.to_dict()}, 200

    # Внести изменения в объект Contract
    # noinspection PyMethodMayBeStatic
    def put(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)
        data = self.parser.parse_args()

        # Если хотят изменить у Contract поле conclusion_date (дата создания)
        if data['conclusion_date'] is not None:
            return {'message': "contracts conclusion date cannot be changed, it's done automatically"}, 409

        # Если данные ничего не изменяют
        if contract.to_dict() == data:
            return {"message": "You have changed nothing"}, 409

        # Проверку на изменнение клиента не делаем

        # Если контракту присваивают application, который уже используется
        if data['application_id'] is not None:
            if Application.query.get_or_404(data['application_id']).contract:
                return {'message': "This application is already in use"}, 409

        contract.from_dict(data)
        db.session.commit()
        return {'data': contract.to_dict()}, 200

    # Удалить объект Contract
    # noinspection PyMethodMayBeStatic
    def delete(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)

        if contract.application.status == 'active':
            return {'message': "This contract has an active application and cannot be deleted"}, 409

        db.session.delete(contract)
        db.session.commit()
        return {'data': contract.to_dict()}, 200


# Посмотреть какую заявку имеет контракт
class ContractApp(Resource):
    # Получить объект Application from Contract
    # noinspection PyMethodMayBeStatic
    def get(self, contract_id):
        contract = Contact.query.get_or_404(contract_id)
        if contract.application is not None:
            app = contract.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got an app"}, 409


# Посмотреть какого клиента имеет контракт
class ContractClient(Resource):
    # Получить объект Application from Contract
    # noinspection PyMethodMayBeStatic
    def get(self, contract_id):
        contract = Contact.query.get_or_404(contract_id)
        if contract.client is not None:
            client = contract.client
            return {'data': client.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got a client"}, 409


""" Заявки (Application) """


# Список всех заявок
class Applications(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True,
                                 help='application name (description) not provided', location='json')
        self.parser.add_argument('conclusion_date', type=str, required=False,
                                 default=datetime.utcnow, location='json')
        self.parser.add_argument('delivery_route', type=int, required=False, location='json')
        self.parser.add_argument('shipper_id', type=int, required=False, location='json')
        self.parser.add_argument('receiver_id', type=int, required=False, location='json')
        self.parser.add_argument('status', type=str, required=False,
                                 default='active', location='json')
        super(Applications, self).__init__()

    # Выдать список всех объектов типа Application
    # noinspection PyMethodMayBeStatic
    def get(self):
        applications_list = Application.query.all()
        data = Application.to_dict_list(applications_list)
        return {'data': data}, 200

    # Добавить новый объект типа Application
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если контактные лица уже привязаны к каким-то заявкам
        if data['shipper_id'] is not None:
            if Application.query.filter_by(shipper_id=data['shipper_id']).first():
                return {'message': "This contact is already in use"}, 409
        if data['receiver_id'] is not None:
            if Application.query.filter_by(receiver_id=data['receiver_id']).first():
                return {'message': "This contact is already in use"}, 409

        # Если такой маршрут уже используется какой-то заявкой
        if Application.query.filter_by(delivery_route=data['delivery_route']).first():
            return {'message': "Please use a different delivery_route (already in use)"}

        application = Application()
        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return {'data': application.to_dict()}, 200


# Одна конкретная заявка
class ApplicationSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=False, location='json')
        self.parser.add_argument('conclusion_date', type=str, required=False, location='json')
        self.parser.add_argument('delivery_route', type=int, required=False, location='json')
        self.parser.add_argument('shipper_id', type=int, required=False, location='json')
        self.parser.add_argument('receiver_id', type=int, required=False, location='json')
        self.parser.add_argument('status', type=str, required=False, location='json')
        super(ApplicationSingle, self).__init__()

    # Получить объект Application
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        application = Application.query.get_or_404(application_id)
        data = application.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Application
    # noinspection PyMethodMayBeStatic
    def put(self, application_id):
        application = Application.query.get_or_404(application_id)
        data = self.parser.parse_args()

        # Если хотят изменить у Application поле delivery_route (маршрут)
        if data['delivery_route'] is not None:
            # Если такой маршрут уже используется
            if Application.query.filter_by(delivery_route=data['delivery_route']).first():
                return {'message': "This delivery route is already in use. Please use a different route"}
            # Если такого маршрута нет
            if not Route.query.get(data['delivery_route']):
                return {'message': "This delivery route doesn't exist. Please use a different route"}

        # Если контактные лица уже привязаны к каким-то заявкам
        if data['shipper_id'] is not None:
            if Application.query.filter_by(shipper_id=data['shipper_id']).first():
                return {'message': "This contact is already in use"}, 409
            # Если такого контакта нет
            if Contact.query.get(data['shipper_id']):
                return {'message': "This contact doesn't exist"}, 409
        if data['receiver_id'] is not None:
            if Application.query.filter_by(receiver_id=data['receiver_id']).first():
                return {'message': "This contact is already in use"}, 409
            # Если такого контакта нет
            if Contact.query.get(data['shipper_id']):
                return {'message': "This contact doesn't exist"}, 409

        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return {'data': application.to_dict()}, 201

    # Удалить объект Application
    # noinspection PyMethodMayBeStatic
    def delete(self, application_id):
        application = Application.query.get_or_404(application_id)

        if application.status == 'active':
            return {'message': "This application is active and cannot be deleted until it's finished"}, 409

        db.session.delete(application)
        db.session.commit()
        return {'data': application.to_dict()}, 200


# Все грузы у конкретной заявки
class ApplicationSingleCargos(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cargos = app.cargos.all()
        data = Cargo.to_dict_list(cargos)
        return {'data': data}, 200


# Все водители у конкретной заявки
class ApplicationsDrivers(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        drivers = app.drivers
        data = Driver.to_dict_list(drivers)
        return {'data': data}, 200


# Все водители у конкретной заявки
class ApplicationsCars(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cars = app.cars
        data = Car.to_dict_list(cars)
        return {'data': data}, 200


""" Водители (Driver) """


# Все водители
class Drivers(Resource):

    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=True,
                                 help='last name not provided', location='json')
        self.parser.add_argument('first_name', type=str, required=True,
                                 help='first name nor provided', location='json')
        self.parser.add_argument('middle_name', type=str, required=False,
                                 default=None, location='json')
        self.parser.add_argument('categories', type=list, required=True,
                                 help='categories not provided', location='json')
        self.parser.add_argument('phone', type=str, required=True,
                                 help='drivers phone not provided', location='json')
        super(Drivers, self).__init__()

    # Выдать список всех объектов Driver
    # noinspection PyMethodMayBeStatic
    def get(self):
        drivers_list = Driver.query.all()
        data = Driver.to_dict_list(drivers_list)
        return {'data': data}, 200

    # Создать новый объект Driver
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если водитель с таким ФИО уже есть
        if Driver.query.filter_by(last_name=data['last_name'], first_name=data['first_name'],
                                  middle_name=data['middle_name']).first():
            return {'message': "This driver already exist. May need to delete..."}, 409

        # Проверка телефона
        if data['phone'] and (len(data['phone']) > 11 or not data['phone'][0] in ['7', '8']):
            return {'message': "Incorrect phone format"}, 409

        if Driver.query.filter_by(phone=data['phone']).first():
            return {'message': "Driver with this phone already exists"}, 409

        driver = Driver()
        driver.from_dict(data)
        db.session.add(driver)
        db.session.commit()
        return {'data': driver.to_dict()}, 201


# Один водитель
class DriverSingle(Resource):

    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('categories', type=list, required=False, location='json')
        super(DriverSingle, self).__init__()

    # Получить объект Driver
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        data = Driver.query.get_or_404(driver_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Driver
    # noinspection PyMethodMayBeStatic
    def put(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        data = self.parser.parse_args()

        # Если данные ничего не изменяют
        if driver.to_dict() == data:
            return {'message': "You have changed nothing"}, 409

        driver.from_dict(data)
        db.session.commit()
        return {'data': driver.to_dict()}, 200

    # Удалить объект Driver
    # noinspection PyMethodMayBeStatic
    def delete(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)

        # Если у водитель есть активный заказ
        applications = driver.applications
        for application in applications:
            if application.status == 'active':
                return {'message': "This driver has an order and cannot be deleted (is not free)"}, 409

        db.session.delete(driver)
        db.session.commit()
        return {'data': driver.to_dict()}, 200


# Все заявки у конкретного водителя
class DriversApplications(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        applications = driver.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200


# Послужной список водителя
class DriversService(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        applications = []
        for application in driver.applications:
            if application.status is 'finished':
                applications.append(application)
        data = Application.to_dict_list(applications)
        return {'data': data}, 200


""" Машины/Грузовики (Cars) """


# Все машины
class Cars(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model', type=str, required=True,
                                 help='model not provided', location='json')
        self.parser.add_argument('category', type=str, required=True,
                                 help='category not provided', location='json')
        self.parser.add_argument('weight', type=float, required=True,
                                 help='weight not provided', location='json')
        self.parser.add_argument('volume', type=float, required=True,
                                 help='volume not provided', location='json')
        super(Cars, self).__init__()

    # Выдать список всех объектов Car
    # noinspection PyMethodMayBeStatic
    def get(self):
        cars_list = Car.query.all()
        data = Car.to_dict_list(cars_list)
        return {'data': data}, 200

    # Создать новый объект Car
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь никаких проверок вроде как нет, так как одинаковых машин может быть несколько
        car = Car()
        car.from_dict(data)
        db.session.add(car)
        db.session.commit()
        return {'data': car.to_dict()}, 201


# Одна машина
class CarSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model', type=str, required=False, location='json')
        self.parser.add_argument('category', type=str, required=False, location='json')
        self.parser.add_argument('weight', type=float, required=False, location='json')
        self.parser.add_argument('volume', type=float, required=False, location='json')
        super(CarSingle, self).__init__()

    # Получить объект Car
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        data = Car.query.get_or_404(car_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Car
    # noinspection PyMethodMayBeStatic
    def put(self, car_id):
        car = Car.query.get_or_404(car_id)
        data = self.parser.parse_args()

        # Если данные ничего не изменяют
        if car.to_dict() == data:
            return {'message': "You have changed nothing"}, 409

        car.from_dict(data)
        db.session.commit()
        return {'data': car.to_dict()}, 200

    # Удалить объект Car
    # noinspection PyMethodMayBeStatic
    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)

        # Если машина в данный момент используется для выполнения заказа
        applications = car.applications
        for application in applications:
            if application.status == 'active':
                return {'message': "This vehicle has an order and cannot be deleted (is not free)"}, 409

        db.session.delete(car)
        db.session.commit()
        return {'data': car.to_dict()}, 200


# Все заявки у конкретной машины
class CarsApplications(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        applications = car.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200


# Послужной список (амортизации) машины
class CarsService(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        applications = []
        for application in car.applications:
            if application.status is 'finished':
                applications.append(application)

        data = Application.to_dict_list(applications)
        return {'data': data}, 200


""" Реквизиты """


# Все реквизиты
class Requisites(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bank_name', type=str, required=True,
                                 help='bank_name not provided', location='json')
        self.parser.add_argument('bank_account', type=str, required=True,
                                 help='bank_account name not provided', location='json')
        self.parser.add_argument('BIK', type=str, required=True,
                                 help='BIK not provided', location='json')
        self.parser.add_argument('INN', type=str, required=True,
                                 help='INN not provided', location='json')
        self.parser.add_argument('KPP', type=str, required=True,
                                 help='KSS not provided', location='json')
        self.parser.add_argument('KS', type=str, required=True,
                                 help='KS not provided', location='json')
        self.parser.add_argument('RS', type=str, required=True,
                                 help='RS not provided', location='json')
        super(Requisites, self).__init__()

    # Выдать список всех объектов Requisite
    # noinspection PyMethodMayBeStatic
    def get(self):
        requisites_list = Requisite.query.all()
        data = Requisite.to_dict_list(requisites_list)
        return {'data': data}, 200

    # Создать новый объект Requisite
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        requisite = Requisite()
        requisite.from_dict(data)
        db.session.add(requisite)
        db.session.commit()
        return {'data': requisite.to_dict()}, 201


# Один реквизит
class RequisiteSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bank_name', type=str, required=False, location='json')
        self.parser.add_argument('bank_account', type=str, required=False, location='json')
        self.parser.add_argument('BIK', type=str, required=False, location='json')
        self.parser.add_argument('INN', type=str, required=False, location='json')
        self.parser.add_argument('KPP', type=str, required=False, location='json')
        self.parser.add_argument('KS', type=str, required=False, location='json')
        self.parser.add_argument('RS', type=str, required=False, location='json')
        super(RequisiteSingle, self).__init__()

    # Получить объект Requisite
    # noinspection PyMethodMayBeStatic
    def get(self, requisite_id):
        data = Requisite.query.get_or_404(requisite_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Requisite
    # noinspection PyMethodMayBeStatic
    def put(self, requisite_id):
        requisite = Requisite.query.get_or_404(requisite_id)
        data = self.parser.parse_args()

        # Если данные ничего не изменяют
        if requisite.to_dict() == data:
            return {'message': "You have changed nothing"}, 409

        requisite.from_dict(data)
        db.session.commit()
        return {'data': requisite.to_dict()}, 200

    # Удалить объект Requisite
    # noinspection PyMethodMayBeStatic
    def delete(self, requisite_id):
        requisite = Requisite.query.get_or_404(requisite_id)

        db.session.delete(requisite)
        db.session.commit()
        return {'data': requisite.to_dict()}, 200


""" Контакты """


# Все контакты
class Contacts(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=True,
                                 help='last name not provided', location='json')
        self.parser.add_argument('first_name', type=str, required=True,
                                 help='first name not provided', location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('organization', type=str, required=False, location='json')
        self.parser.add_argument('position', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=True,
                                 help='phone not provided', location='json')
        super(Contacts, self).__init__()

    # Выдать список всех объектов Contact
    # noinspection PyMethodMayBeStatic
    def get(self):
        contacts_list = Contact.query.all()
        data = Contact.to_dict_list(contacts_list)
        return {'data': data}, 200

    # Создать новый объект Contact
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Проверка на правильность телефонного номера
        if len(data['phone']) > 11 or not data['phone'][0] == '7':
            return {'message': "Incorrect phone format"}, 409

        # Если контакт с таким телефоном уже есть
        if Contact.query.filter_by(phone=data['phone']).first():
            return {'message': "Contact with this phone already exists"}, 409

        contact = Contact()
        contact.from_dict(data)
        db.session.add(contact)
        db.session.commit()
        data = contact.to_dict()
        return {'data': data}, 201


# Один контакт
class ContactSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('organization', type=str, required=False, location='json')
        self.parser.add_argument('position', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=False, location='json')
        super(ContactSingle, self).__init__()

    # Получить объект Contact
    # noinspection PyMethodMayBeStatic
    def get(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        data = contact.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Contact
    # noinspection PyMethodMayBeStatic
    def put(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        data = self.parser.parse_args()

        # Проверка на правильность телефонного номера
        if data['phone'] and (len(data['phone']) > 11 or not data['phone'][0] in ['7', '8']):
            return {'message': "incorrect phone format"}, 409

        # Если контакт с таким телефоном уже есть
        _tempContact = Contact.query.filter_by(phone=data['phone']).first()
        if contact.contact_id != _tempContact.contact_id:
            return {'message': "Contact with this phone already exists"}, 409

        contact.from_dict(data)
        db.session.commit()
        return {'data': contact.to_dict()}, 200

    # Удалить объект Contact
    # noinspection PyMethodMayBeStatic
    def delete(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)

        db.session.delete(contact)
        db.session.commit()
        data = contact.to_dict()
        return {'data': data}, 200


# Информация о том какой груз (заявку) ожидает контакт
class ContactApp(Resource):
    # Получить объект Application from Contact
    # noinspection PyMethodMayBeStatic
    def get(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)

        # Проверяем есть ли у контакта привязка к заявке
        if contact.application_receive is not None:
            app = contact.application_receive
            return {'data': app.to_dict()}, 200
        if contact.application_shipp is not None:
            app = contact.application_shipp
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This contact isn't linked to an app"}, 409


""" Маршруты """


# Список маршрутов
class Routes(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('delivery_address', type=str, required=True,
                                 help='delivery_address not provided', location='json')
        self.parser.add_argument('shipping_address', type=str, required=True,
                                 help='shipping_address not provided', location='json')
        self.parser.add_argument('distance', type=float, required=False, location='json')
        self.parser.add_argument('estimated_time', type=int, required=False, location='json')
        super(Routes, self).__init__()

    # Выдать список всех объектов Route
    # noinspection PyMethodMayBeStatic
    def get(self):
        routes_list = Route.query.all()
        data = Route.to_dict_list(routes_list)
        return {'data': data}, 200

    # Создать новый объект Route
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        route = Route()
        route.from_dict(data)
        db.session.add(route)
        db.session.commit()
        data = route.to_dict()
        return {'data': data}, 201


# Один маршрут
class RouteSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('delivery_address', type=str, required=False, location='json')
        self.parser.add_argument('shipping_address', type=str, required=False, location='json')
        self.parser.add_argument('distance', type=float, required=False, location='json')
        self.parser.add_argument('estimated_time', type=int, required=False, location='json')
        super(RouteSingle, self).__init__()

    # Получить объект Route
    # noinspection PyMethodMayBeStatic
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        data = route.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Route
    # noinspection PyMethodMayBeStatic
    def put(self, route_id):
        route = Route.query.get_or_404(route_id)
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        route.from_dict(data)
        db.session.commit()
        return {'data': route.to_dict()}, 200

    # Удалить объект Route
    # noinspection PyMethodMayBeStatic
    def delete(self, route_id):
        route = Route.query.get_or_404(route_id)

        db.session.delete(route)
        db.session.commit()
        data = route.to_dict()
        return {'data': data}, 200


# Посмотреть к какой заявке привязан маршрут
class RouteApp(Resource):
    # Получить объект Application from Route
    # noinspection PyMethodMayBeStatic
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        if route.application is not None:
            app = route.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This route hasn't got an app"}, 409


""" ГРУЗЫ 200 """


# Список всех грузов
class Cargos(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nomenclature', type=str, required=True,
                                 help='nomenclature not provided', location='json')  # Что такое 'nomenclature'??
        self.parser.add_argument('weight', type=float, required=True,
                                 help='weight not provided', location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        super(Cargos, self).__init__()

    # Выдать список всех объектов Cargo
    # noinspection PyMethodMayBeStatic
    def get(self):
        cargos_list = Cargo.query.all()
        data = Cargo.to_dict_list(cargos_list)
        return {'data': data}, 200

    # Создать новый объект Cargo
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        cargo = Cargo()
        cargo.from_dict(data)
        db.session.add(cargo)
        db.session.commit()
        data = cargo.to_dict()
        return {'data': data}, 201


# Один груз
class CargoSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nomenclature', type=str, required=False, location='json')  # Что такое 'nomenclature'?
        self.parser.add_argument('weight', type=float, required=False, location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        super(CargoSingle, self).__init__()

    # Получить объект Cargo
    # noinspection PyMethodMayBeStatic
    def get(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)
        data = cargo.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Cargo
    # noinspection PyMethodMayBeStatic
    def put(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)
        data = self.parser.parse_args()
        # Здесь проверку на что-либо делать незачем

        cargo.from_dict(data)
        db.session.commit()
        return {'data': cargo.to_dict()}, 200

    # Удалить объект Cargo
    # noinspection PyMethodMayBeStatic
    def delete(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)

        # Если удаляют груз, заявка к которой он прикрепен уже выполнена
        if cargo.application is not None and cargo.application.status == 'finished':
            return {'message': "Cannot delete cargo that has a finished app"}, 409

        db.session.delete(cargo)
        db.session.commit()
        data = cargo.to_dict()
        return {'data': data}, 200


# Посмотреть к какой заявке привязан груз
class CargoApp(Resource):
    # Получить объект Application from Cargo
    # noinspection PyMethodMayBeStatic
    def get(self, cargo_id):
        cargo = Route.query.get_or_404(cargo_id)
        if cargo.application is not None:
            app = cargo.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This cargo isn't in an app"}, 409
