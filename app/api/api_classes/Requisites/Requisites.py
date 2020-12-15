from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Requisite
from app.api.api_classes import db


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
        return {'data': requisite.to_dict(), 'message': "Реквизит успешно создан"}, 201
