from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Client
from app.api.api_classes import db
from app.api.extensions import compare


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

        # Проверяем какие поля хотят изменить запросом
        result = compare(client.to_dict()['attributes'], data)

        for attribute in result.keys():
            if not result[attribute] and data[attribute] is not None:
                # Если изменяют телефон
                if attribute == 'phone':

                    # Проверка на правильность телефонного номера
                    if len(data[attribute]) > 11 or data[attribute][0] not in ['7', '8']:
                        return {'message': "incorrect phone format"}, 409

                    # Если клиент с таким телефоном уже есть
                    if Client.query.filter_by(phone=data[attribute]).first():
                        return {'message': "Client with this phone already exists"}, 409

                # Если изменяют e-mail
                elif attribute == 'email':

                    # Если клиент с таким e-mail уже есть
                    if Client.query.filter_by(email=data['email']).first():
                        return {'message': "Client with this e-mail address already exists"}, 409

                # Если изменяют номер паспорта
                elif attribute == 'passport_number':

                    # Если пытаются поменять клиенту номер паспорта, а такая комбинация уже есть у другого клиента
                    if Client.query.filter_by(passport_number=data['passport_number'],
                                              passport_series=client.passport_series).first():
                        return {'message': "Client cannot have passport data that already exists (passport number bad)"}, 409  # noqa

                # Если изменяют серию паспорта
                elif attribute == 'passport_series':

                    # Если пытаются поменять клиенту серию паспорта, а такая комбинация уже есть у другого клиента
                    if Client.query.filter_by(passport_number=client.passport_number,
                                              passport_series=data['passport_series']).first():
                        return {
                                   'message': "Client cannot have passport data that already exists (passport series bad)"}, 409  # noqa

                # Если изменяют что-то из ФИО
                elif attribute in ['first_name', 'last_name', 'middle_name']:
                    if Client.query.filter_by(first_name=data[attribute],
                                              last_name=data[attribute],
                                              middle_name=data[attribute]).first():
                        return {'message': "Client with this full name already exists"}, 409

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
