from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Cargo, Application
from app.api.api_classes import db


# Список всех грузов
class Cargos(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nomenclature', type=str, required=True,
                                 help='nomenclature not provided', location='json')  # Что такое 'nomenclature'??
        self.parser.add_argument('weight', type=float, required=True,
                                 help='weight not provided', location='json')
        self.parser.add_argument('application_id', type=int, required=False, location='json')
        super(Cargos, self).__init__()

    # Выдать список всех объектов Cargo
    # noinspection PyMethodMayBeStatic
    def get(self):
        cargos_list = Cargo.query.all()
        data = Cargo.to_dict_list(cargos_list)
        return {'data': data}, 200

    # Создать новый объект Cargo
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        for attribute in data.keys():
            if data[attribute] is not None:
                if attribute == 'nomenclature':
                    if len(data[attribute]) > 64:
                        return {'message': "Name length cannot be bigger than 64"}, 409
                if attribute == 'weight':
                    if data[attribute] < 0.0:
                        return {'message': "Weight cannot be lower than zero"}, 409
                if attribute == 'application_id':
                    if not Application.query.get(data[attribute]):
                        return {'message': "Application doesn't exist"}, 409
            else:
                if attribute in ['nomenclature', 'weight']:
                    return {'message': "Field {} cannot be null".format(attribute)}, 409

        cargo = Cargo()
        cargo.from_dict(data)
        db.session.add(cargo)
        db.session.commit()
        data = cargo.to_dict()
        return {'data': data, 'message': "Груз успешно создан"}, 201
