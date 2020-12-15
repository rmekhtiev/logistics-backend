from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Cargo, Application
from app.api.api_classes import db
from app.api.extensions import compare


# Один груз
class CargoSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nomenclature', type=str, required=False, location='json')  # Что такое 'nomenclature'?
        self.parser.add_argument('weight', type=float, required=False, location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        super(CargoSingle, self).__init__()

    # Получить объект Cargo
    # noinspection PyMethodMayBeStatic
    def get(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)
        data = cargo.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Cargo
    # noinspection PyMethodMayBeStatic
    def put(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        result = compare(cargo.to_dict()['attributes'], data)

        for argument in result.keys():
            if not result[argument]:
                # Проверка на прикрпеление груза к завершённой заявке
                if argument == 'application_id':
                    application = Application.query.get_or_404(data[argument])
                    if application.status == 'finished':
                        return {'message': "Cannot assign a cargo to a finished application"}, 409

        cargo.from_dict(data)
        db.session.commit()
        return {'data': cargo.to_dict(), 'message': "Груз №{} успешно изменён".format(cargo_id)}, 200

    # Удалить объект Cargo
    # noinspection PyMethodMayBeStatic
    def delete(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)

        # Если удаляют груз, заявка к которой он прикрепен уже выполнена
        if cargo.application is not None and cargo.application.status == 'finished':
            return {'message': "Cannot delete cargo that has a finished app"}, 409

        db.session.delete(cargo)
        db.session.commit()
        data = cargo.to_dict()
        return {'data': data, 'message': "Груз №{} успешно удалён".format(cargo_id)}, 200
