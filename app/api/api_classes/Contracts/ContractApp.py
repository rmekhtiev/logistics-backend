from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Contract


# Посмотреть какую заявку имеет контракт
from app.api.api_documentation.ContractItem import ContractItem


class ContractApp(Resource):
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
        if contract.application is not None:
            app = contract.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This contract hasn't got an app"}, 409
