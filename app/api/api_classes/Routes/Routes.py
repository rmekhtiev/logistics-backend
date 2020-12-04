from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Route
from app.api.api_classes import db


# Список маршрутов
class Routes(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('delivery_address', type=str, required=True,
                                 help='delivery_address not provided', location='json')
        self.parser.add_argument('shipping_address', type=str, required=True,
                                 help='shipping_address not provided', location='json')
        self.parser.add_argument('distance', type=float, required=False, location='json')
        self.parser.add_argument('estimated_time', type=int, required=False, location='json')
        super(Routes, self).__init__()

    # Выдать список всех объектов Route
    # noinspection PyMethodMayBeStatic
    def get(self):
        routes_list = Route.query.all()
        data = Route.to_dict_list(routes_list)
        return {'data': data}, 200

    # Создать новый объект Route
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        route = Route()
        route.from_dict(data)
        db.session.add(route)
        db.session.commit()
        data = route.to_dict()
        return {'data': data}, 201
