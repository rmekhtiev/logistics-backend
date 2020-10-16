from flask import request, jsonify, url_for
from flask_restful import Resource, reqparse
from app import db
from app.models import *


class HelloWorld(Resource):
    def get(self):
        return {'Test message': 'Hello World'}

    def post(self):
        json_in = request.get_json()
        return {'you sent': json_in}, 201


class Multi(Resource):
    def get(self, num):
        return {'result': num * 10}


""" Заявки """


# Список всех заявок
class ApplicationsList(Resource):
    def get(self):
        applications_list = Application.query.all()
        data = Application.to_dict_list(applications_list)
        return jsonify(data)

    def post(self):
        data = request.get_json() or {}
        for column in ['name', 'conclusion_date', 'delivery_route', 'payment_detail']:
            if column not in data:
                # + 'must include name, conclusion date, delivery route and payment'
                return jsonify(data)
        if Application.query.filter_by(delivery_route=data['delivery_route']).first():
            return 'please use a different delivery_route (already exist)'
        if Application.query.filter_by(payment_detail=data['payment_detail']).first():
            return 'please use a different payment_detail (already exist)'
        application = Application()
        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return jsonify(application.to_dict(False))


# Одна конкретная заявка
class ApplicationSingle(Resource):
    def get(self, application_id):
        data = Application.query.get_or_404(application_id).to_dict(JOIN=True)
        return jsonify(data)

    def put(self, application_id):
        application = Application.query.get_or_404(application_id)
        data = request.get_json() or {}

        # Если хотят изменить у Application поле delivery_route (маршрут)
        if 'delivery_route' in data:
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
            # Если такой оплаты нет
            if not Payment.query.get(data['payment_detail']):
                return "This payment detail doesn't exist. Please use a different payment"

        application = Application()
        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return jsonify(application.to_dict(False))


# Все грузы у конкретной заявки
class ApplicationSingleCargos(Resource):
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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('last_name', type=str, required=True,
                                   help='last name not provided', location='json')
        self.reqparse.add_argument('first_name', type=str, required=True,
                                   help='first name nor provided', location='json')
        self.reqparse.add_argument('middle_name', type=str, required=False,
                                   default=None, location='json')
        self.reqparse.add_argument('categories', type=list, required=True,
                                   help='categories not provided', location='json')
        self.reqparse.add_argument('is_free', type=bool, required=False,
                                   default=True, location='json')
        super(Drivers, self).__init__()

    # Выдать список всех объектов Driver
    def get(self):
        drivers_list = Driver.query.all()
        data = Driver.to_dict_list(drivers_list)
        return data, 200

    # Создать новый объект Driver
    def post(self):
        data = self.reqparse.parse_args()

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
    # Получить объект Driver
    def get(self, driver_id):
        data = Driver.query.get_or_404(driver_id).to_dict()
        return data, 200

    # Внести изменения в объект Driver
    def put(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        data = request.get_json() or {}

        # Если хотят изменить у Driver поле is_free (статус свободен)
        if 'is_free' in data and driver.is_free != data['is_free']:
            return "Drivers status can not be changed manually, it's done automatically"

        # Если данные ничего не изменяют
        if driver.to_dict() == data:
            return "You have changed nothing"
        else:
            driver.from_dict(data)
        db.session.commit()
        return driver.to_dict(), 200

    # Удалить объект Driver
    def delete(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        if not driver.is_free:
            return {'message': 'This driver has an order and cannot be deleted (is not free)'}, 409
        else:
            db.session.delete(driver)
            db.session.commit()
        return driver.to_dict(), 200


class Cars(Resource):
    def get(self):
        cars_list = Car.query.all()
        data = Car.to_dict_list(cars_list)
        return jsonify(data)

    def post(self):
        data = request.get_json() or {}
        for column in ['weight', 'volume', 'model', 'category']:
            if column not in data:
                return 'must include model, category, weight and volume'
        car = Car()
        car.from_dict(data)
        db.session.add(car)
        db.session.commit()
        return jsonify(car.to_dict())
