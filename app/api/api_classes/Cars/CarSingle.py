from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Car
from app.api.api_classes import db


# Одна машина
class CarSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model', type=str, required=False, location='json')
        self.parser.add_argument('category', type=str, required=False, location='json')
        self.parser.add_argument('weight', type=float, required=False, location='json')
        self.parser.add_argument('volume', type=float, required=False, location='json')
        super(CarSingle, self).__init__()

    # Получить объект Car
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        data = Car.query.get_or_404(car_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Car
    # noinspection PyMethodMayBeStatic
    def put(self, car_id):
        car = Car.query.get_or_404(car_id)
        data = self.parser.parse_args()
        car.from_dict(data)
        db.session.commit()
        return {'data': car.to_dict(), 'message': "Машина №{} успешно изменена".format(car_id)}, 200

    # Удалить объект Car
    # noinspection PyMethodMayBeStatic
    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)

        # Если машина в данный момент используется для выполнения заказа
        applications = car.applications
        for application in applications:
            if application.status == 'active':
                return {'message': "This vehicle has an order and cannot be deleted (is not free)"}, 409

        db.session.delete(car)
        db.session.commit()
        return {'data': car.to_dict(), 'message': "Машина №{} успешно удалена".format(car_id)}, 200
