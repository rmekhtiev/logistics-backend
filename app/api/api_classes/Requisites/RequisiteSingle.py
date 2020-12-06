from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Requisite
from app.api.api_classes import db


# Один реквизит
class RequisiteSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bank_name', type=str, required=False, location='json')
        self.parser.add_argument('bank_account', type=str, required=False, location='json')
        self.parser.add_argument('BIK', type=str, required=False, location='json')
        self.parser.add_argument('INN', type=str, required=False, location='json')
        self.parser.add_argument('KPP', type=str, required=False, location='json')
        self.parser.add_argument('KS', type=str, required=False, location='json')
        self.parser.add_argument('RS', type=str, required=False, location='json')
        super(RequisiteSingle, self).__init__()

    # Получить объект Requisite
    # noinspection PyMethodMayBeStatic
    def get(self, requisite_id):
        data = Requisite.query.get_or_404(requisite_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Requisite
    # noinspection PyMethodMayBeStatic
    def put(self, requisite_id):
        requisite = Requisite.query.get_or_404(requisite_id)
        data = self.parser.parse_args()

        # Проверка на то, что заказ уже выполнен (вместо изменения лучше добавлять новый реквизит)
        for contract in requisite.contracts:
            if contract.requisite == requisite and contract.application.status == 'finished':
                return {'message': "Cannot change anything, when the any application is finished (create new requisite, not change"}, 409 # noqa

        requisite.from_dict(data)
        db.session.commit()
        return {'data': requisite.to_dict(), 'message': "Реквизит №{} успешно изменён".format(requisite_id)}, 200

    # Удалить объект Requisite
    # noinspection PyMethodMayBeStatic
    def delete(self, requisite_id):
        requisite = Requisite.query.get_or_404(requisite_id)

        db.session.delete(requisite)
        db.session.commit()
        return {'data': requisite.to_dict(), 'message': "Реквизит №{} успешно удалён".format(requisite_id)}, 200
