from flask import request, jsonify, url_for
from flask_restful import Resource
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
