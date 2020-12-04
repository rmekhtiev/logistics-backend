from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Car
from app.api.api_classes import db


# Все машины
class Cars(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model', type=str, required=True,
                                 help='model not provided', location='json')
        self.parser.add_argument('category', type=str, required=True,
                                 help='category not provided', location='json')
        self.parser.add_argument('weight', type=float, required=True,
                                 help='weight not provided', location='json')
        self.parser.add_argument('volume', type=float, required=True,
                                 help='volume not provided', location='json')
        super(Cars, self).__init__()

    # Выдать список всех объектов Car
    # noinspection PyMethodMayBeStatic
    def get(self):
        cars_list = Car.query.all()
        data = Car.to_dict_list(cars_list)
        return {'data': data}, 200

    # Создать новый объект Car
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = self.parser.parse_args()

        # Здесь никаких проверок вроде как нет, так как одинаковых машин может быть несколько
        # todo сделать проверку на null поля
        car = Car()
        car.from_dict(data)
        db.session.add(car)
        db.session.commit()
        return {'data': car.to_dict()}, 201
