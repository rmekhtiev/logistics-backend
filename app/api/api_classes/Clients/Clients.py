from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Client
from app.api.api_classes import db


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

        for attribute in data.keys():
            if data[attribute] is not None:
                if attribute in ['passport_number', 'passport_series']:
                    if Client.query.filter_by(passport_number=data['passport_number'],
                                              passport_series=data['passport_series']).first():
                        return {'message': "Client with that passport data already exists"}, 409
                if attribute in ['last_name', 'first_name', 'middle_name']:
                    if Client.query.filter_by(last_name=data['last_name'],
                                              first_name=data['first_name'],
                                              middle_name=data['middle_name']).first():
                        return {'message': "Client with this full name already exists"}, 409
                if attribute == 'phone':
                    # Проверка на правильность телефонного номера
                    if len(data['phone']) > 11 or data['phone'][0] != '7':
                        return {'message': "Incorrect phone format"}, 409
                    # Если клиент с таким телефоном уже есть
                    if Client.query.filter_by(phone=data['phone']).first():
                        return {'message': "Client with this phone already exists"}, 409
                if attribute == 'email':
                    # Если клиент с таким e-mail уже есть
                    if Client.query.filter_by(email=data['email']).first():
                        return {'message': "Client with this e-mail address already exists"}, 409
            else:
                if attribute in ['passport_number', 'passport_series', 'last_name', 'first_name', 'phone']:
                    return {'message': "Field '{}' cannot be null".format(attribute)}

        client = Client()
        client.from_dict(data)
        db.session.add(client)
        db.session.commit()
        data = client.to_dict()
        return {'data': data}, 201
