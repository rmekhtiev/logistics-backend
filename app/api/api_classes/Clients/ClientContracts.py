from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Client, Contract


# Список всех контрактов, которые заключал клиент с компанией
from app.api.api_documentation.ClientItem import ClientItem


class ClientContracts(Resource):
    # Вывести список всех Contract у данного Client
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a clients list',
        summary="",
        nickname="Clients GET",
        responseClass=ClientItem.__name__,
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
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        contracts = client.contracts
        return {'data': Contract.to_dict_list(contracts)}, 200
