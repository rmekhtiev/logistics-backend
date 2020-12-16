from flask_restful_swagger import swagger

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Client, Contract, Application, Requisite
from app.api.api_classes import db, datetime


# Список всех контрактов
from app.api.api_documentation.ContractItem import ContractItem


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
                                 default='Card', location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        self.parser.add_argument('requisite_id', type=int, required=False, location='json')

        super(Contracts, self).__init__()

    # Выдать список всех объектов типа Contract
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a contracts list',
        summary="",
        nickname="Contracts GET",
        responseClass=ContractItem.__name__,
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Success"
            },
            {
                "code": 404,
                "message": "Not Found"
            }
        ]
    )
    def get(self):
        contracts_list = Contract.query.all()
        data = Contract.to_dict_list(contracts_list)
        return {'data': data}, 200

    # Добавить новый объект типа Contract
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create a contract',
        summary="",
        nickname="Contracts POST",
        responseClass=ContractItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": ContractItem.properties,
                "required": True
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def post(self):
        data = self.parser.parse_args()

        for attribute in data.keys():
            if data[attribute] is not None:
                if attribute == 'conclusion_date':
                    if data[attribute] > datetime.utcnow():
                        return {'message': "Provided datetime is bigger than existing {date}".format(date=datetime.utcnow())} # noqa
                if attribute == 'cost':
                    if data[attribute] < 0.0:
                        return {'message': "Cost cannot be lower than zero"}, 409
                if attribute == 'client_id':
                    if not Client.query.get(data[attribute]):
                        return {'message': "This client doesn't exist"}, 409
                if attribute == 'payment_type':
                    if data[attribute].lower() not in ['card', 'cash', 'transfer']:
                        return {'message': "Payment type incorrect"}, 409
                if attribute == 'application_id':
                    if not Application.query.get(data[attribute]):
                        return {'message': "Application not found"}, 409
                    else:
                        app = Application.query.get(data[attribute])
                        if app.status == 'finished':
                            return {'message': "The application given is finished"}, 409
                        if app.contract is not None:
                            return {'message': "The application given is already in use"}, 409
                if attribute == 'requisite_id':
                    if not Requisite.query.get(data[attribute]):
                        return {'message': "Requisite not found"}, 409
            else:
                if attribute in ['cost']:
                    return {'message': "Field '{}' cannot be null".format(attribute)}

        contract = Contract()
        contract.from_dict(data)
        db.session.add(contract)
        db.session.commit()
        return {'data': contract.to_dict(), 'message': "Контракт успешно добавлен"}, 200
