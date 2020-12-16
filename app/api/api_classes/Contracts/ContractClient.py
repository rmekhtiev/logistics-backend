from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Contract


# Посмотреть какого клиента имеет контракт
from app.api.api_documentation.ContractItem import ContractItem


class ContractClient(Resource):
    # Получить объект Application from Contract
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
    def get(self, contract_id):
        contract = Contract.query.get_or_404(contract_id)
        if contract.client is not None:
            client = contract.client
            return {'data': client.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got a client"}, 409
