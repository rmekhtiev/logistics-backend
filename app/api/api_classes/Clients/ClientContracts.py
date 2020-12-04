from app.api.api_classes import Resource
from app.api.api_classes import Client, Contract


# Список всех контрактов, которые заключал клиент с компанией
class ClientContracts(Resource):
    # Вывести список всех Contract у данного Client
    # noinspection PyMethodMayBeStatic
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        contracts = client.contracts
        return {'data': Contract.to_dict_list(contracts)}, 200
