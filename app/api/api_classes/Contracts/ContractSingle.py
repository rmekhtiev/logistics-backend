from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Client, Contract, Application, Requisite
from app.api.api_classes import db
from app.api.extensions import compare


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
        contract = Contract.query.get_or_404(contract_id)
        return {'data': contract.to_dict()}, 200

    # Внести изменения в объект Contract
    # noinspection PyMethodMayBeStatic
    def put(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)
        data = self.parser.parse_args()

        result = compare(contract.to_dict()['attributes'], data)
        for attribute in result.keys():
            if not result[attribute]:
                # Если меняют что-то, а заявка уже выполнена
                if contract.application is not None and contract.application.status == 'finished':
                    return {'message': "Cannot change anything, detached application is already finished"}, 409

                if data[attribute] is not None:
                    # Если хотят изменить у Contract поле conclusion_date (дата создания)
                    if attribute == 'conclusion_date':
                        return {'message': "Contracts conclusion date cannot be changed, it's done automatically"}, 409
                    # Если меняют стоимость
                    if attribute == 'cost':
                        if data[attribute] < 0.0:
                            return {'message': "Cost cannot be lower than zero"}, 409
                    # Если меняют клиента
                    if attribute == 'client_id':
                        if not Client.query.get(data[attribute]):
                            return {'message': "This client doesn't exist"}, 409
                    # Если меняют тип оплаты
                    if attribute == 'payment_type':
                        if data[attribute].lower() not in ['card', 'cash', 'transfer']:
                            return {'message': "Payment type incorrect"}, 409
                    # Если меняют заявку
                    if attribute == 'application_id':
                        app = Application.query.get(data[attribute])
                        # Если переданная заявка не существует
                        if app is None:
                            return {'message': "Application not found"}, 409
                        # Если переданная заявка уже завершена
                        if app.status == 'finished':
                            return {'message': "The application given is finished"}, 409
                        # Если переданная заявка имеет у себя свой контракт
                        if app.contract is not None:
                            return {'message': "The application given has an active contract, please remove it first"}, 409 # noqa
                    # Если меняют реквизиты
                    if attribute == 'requisite_id':
                        if not Requisite.query.get(data[attribute]):
                            return {'message': "Requisite not found"}, 409

        contract.from_dict(data)
        db.session.commit()
        return {'data': contract.to_dict()}, 200

    # Удалить объект Contract
    # noinspection PyMethodMayBeStatic
    def delete(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)

        if contract.application is not None and contract.application.status == 'active':
            return {'message': "This contract has an active application and cannot be deleted"}, 409

        db.session.delete(contract)
        db.session.commit()
        return {'data': contract.to_dict()}, 200
