from app.api.api_classes import Resource
from app.api.api_classes import Contract


# Посмотреть какую заявку имеет контракт
class ContractApp(Resource):
    # Получить объект Application from Contract
    # noinspection PyMethodMayBeStatic
    def get(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)
        if contract.application is not None:
            app = contract.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got an app"}, 409
