from flask import request, jsonify
from flask_restful import Resource, reqparse
from app.models import *

""" Хуй пойми что, Семён пидарас """


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
        return data, 200

    # Создать новый объект Client
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если клиент с такими паспортными данными уже существует
        if Client.query.filter_by(passport_number=data['passport_number'], passport_series=data['passport_series']).first(): # noqa
            return {'message': "Client with that passport data already exists"}, 409

        # Если клиент с таким телефоном уже есть
        if Client.query.filter_by(phone=data['phone']).first():
            return {'message': "Client with this phone already exists"}, 409

        client = Client()
        client.from_dict(data)
        db.session.add(client)
        db.session.commit()
        return client.to_dict(), 201


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
        return data, 200

    # Внести изменения в объект Client
    # noinspection PyMethodMayBeStatic
    def put(self, client_id):
        client = Client.query.get_or_404(client_id)
        data = self.parser.parse_args()

        # Если клиент с такими паспортными данными уже существует
        if Client.query.filter_by(passport_number=data['passport_number'], passport_series=data['passport_series']).first(): # noqa
            return {'message': "Client with that passport data already exists"}, 409

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
        return client.to_dict(), 201

    # Удалить объект Client
    # noinspection PyMethodMayBeStatic
    def delete(self, client_id):
        client = Client.query.get_or_404(client_id)

        # Если хотят удалить клиента, у которого есть активные контракты TODO: поменять is_finished на status
        client_contracts = client.contracts
        for contract in client_contracts:
            if not contract.application.is_finished:
                return {'message': "Cannot delete client with an active contract"}, 409

        db.session.delete(client)
        db.session.commit()
        return client.to_dict(), 200


# Список всех контрактов, которые заключал клиент с компанией
class ClientContracts(Resource):
    # Вывести список всех Contract у данного Client
    # noinspection PyMethodMayBeStatic
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        contracts = client.contracts
        return Contract.to_dict_list(contracts), 200


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
                return {'message': "this application is already in use"}, 409

        contract.from_dict(data)
        db.session.commit()
        return {'data': contract.to_dict()}, 201

    # Удалить объект Contract
    # noinspection PyMethodMayBeStatic
    def delete(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)

        # TODO: Сделать проверку на то, использует ли контракт невыполненную заявку

        db.session.delete(contract)
        db.session.commit()
        return {'data': contract.to_dict()}, 200


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
                return {'message': "this contact is already in use"}, 409
        if data['receiver_id'] is not None:
            if Application.query.filter_by(receiver_id=data['receiver_id']).first():
                return {'message': "this contact is already in use"}, 409

        # Если такой маршрут уже используется какой-то заявкой
        if Application.query.filter_by(delivery_route=data['delivery_route']).first():
            return {'message': "please use a different delivery_route (already in use)" }

        application = Application()
        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return {'data': application.to_dict(False)}, 200


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
        data = application.to_dict(JOIN=False)
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
                return 'This delivery route is already in use. Please use a different route'
            # Если такого маршрута нет
            if not Route.query.get(data['delivery_route']):
                return "This delivery route doesn't exist. Please use a different route"

        # Если хотят изменить у Application поле payment_detail (оплата)
        if 'payment_detail' in data:
            # Если такая оплата уже используется
            if Application.query.filter_by(payment_detail=data['payment_detail']).first():
                return 'This payment detail is already in use. Please use a different payment'

        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return jsonify(application.to_dict(False))


# Все грузы у конкретной заявки
class ApplicationSingleCargos(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cargos = app.cargos.all()
        data = Cargo.to_dict_list(cargos)
        return jsonify(data)


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
        self.parser.add_argument('is_free', type=bool, required=False,
                                 default=True, location='json')
        super(Drivers, self).__init__()

    # Выдать список всех объектов Driver
    # noinspection PyMethodMayBeStatic
    def get(self):
        drivers_list = Driver.query.all()
        data = Driver.to_dict_list(drivers_list)
        return {"data": data}, 200

    # Создать новый объект Driver
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Если водитель с таким ФИО уже есть
        if Driver.query.filter_by(last_name=data['last_name'], first_name=data['first_name'],
                                  middle_name=data['middle_name']).first():
            return 'This driver already exist. May need to delete...'

        driver = Driver()
        driver.from_dict(data)
        db.session.add(driver)
        db.session.commit()
        return driver.to_dict(), 200


# Один водитель
class DriverSingle(Resource):

    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('categories', type=list, required=False, location='json')
        self.parser.add_argument('is_free', type=bool, required=False, location='json')
        super(DriverSingle, self).__init__()

    # Получить объект Driver
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        data = Driver.query.get_or_404(driver_id).to_dict()
        return data, 200

    # Внести изменения в объект Driver
    # noinspection PyMethodMayBeStatic
    def put(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        data = self.parser.parse_args()

        # Если хотят изменить у Driver поле is_free (статус свободен)
        if 'is_free' in data and driver.is_free != data['is_free']:
            return {'message': "Drivers status can not be changed manually, it's done automatically"}, 409

        # Если данные ничего не изменяют
        if driver.to_dict() == data:
            return {'message': "You have changed nothing"}, 409

        driver.from_dict(data)
        db.session.commit()
        return driver.to_dict(), 200

    # Удалить объект Driver
    # noinspection PyMethodMayBeStatic
    def delete(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)

        # Если водитель сейчас выполняет заказ
        if not driver.is_free:
            return {'message': 'This driver has an order and cannot be deleted (is not free)'}, 409

        db.session.delete(driver)
        db.session.commit()
        return driver.to_dict(), 200


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
        self.parser.add_argument('is_free', type=bool, required=False,
                                 default=True, location='json')
        super(Cars, self).__init__()

    # Выдать список всех объектов Car
    # noinspection PyMethodMayBeStatic
    def get(self):
        cars_list = Car.query.all()
        data = Car.to_dict_list(cars_list)
        return data, 200

    # Создать новый объект Car
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь никаких проверок вроде как нет, так как одинаковых машин может быть несколько
        car = Car()
        car.from_dict(data)
        db.session.add(car)
        db.session.commit()
        return car.to_dict(), 201


# Одна машина
class CarSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model', type=str, required=False, location='json')
        self.parser.add_argument('category', type=str, required=False, location='json')
        self.parser.add_argument('weight', type=float, required=False, location='json')
        self.parser.add_argument('volume', type=float, required=False, location='json')
        self.parser.add_argument('is_free', type=bool, required=False, location='json')
        super(CarSingle, self).__init__()

    # Получить объект Car
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        data = Car.query.get_or_404(car_id).to_dict()
        return data, 200

    # Внести изменения в объект Car
    # noinspection PyMethodMayBeStatic
    def put(self, car_id):
        car = Car.query.get_or_404(car_id)
        data = self.parser.parse_args()

        # Если хотят изменить у Car поле is_free (статус свободен)
        if 'is_free' in data and car.is_free != data['is_free']:
            return {"message": "Cars status can not be changed manually, it's done automatically"}, 409

        # Если данные ничего не изменяют
        if car.to_dict() == data:
            return {"message": "You have changed nothing"}, 409

        car.from_dict(data)
        db.session.commit()
        return car.to_dict(), 200

    # Удалить объект Car
    # noinspection PyMethodMayBeStatic
    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)

        # Если машина в данный момент используется для выполнения заказа TODO: 'is_finished' change to 'status'
        if not car.is_free:
            return {'message': 'This vehicle has an order and cannot be deleted (is not free)'}, 409

        db.session.delete(car)
        db.session.commit()
        return car.to_dict(), 200
