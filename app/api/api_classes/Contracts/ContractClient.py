from app.api.api_classes import Resource
from app.api.api_classes import Contract


# Посмотреть какого клиента имеет контракт
class ContractClient(Resource):
    # Получить объект Application from Contract
    # noinspection PyMethodMayBeStatic
    def get(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)
        if contract.client is not None:
            client = contract.client
            return {'data': client.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got a client"}, 409
