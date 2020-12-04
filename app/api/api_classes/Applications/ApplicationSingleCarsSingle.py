from app.api.api_classes import Resource
from app.api.api_classes import Application, Car
from app.api.api_classes import db


# Конкретная машина у конкретной заявки
class ApplicationSingleCarSingle(Resource):
    # прикрепить к данной Application объект Car
    # noinspection PyMethodMayBeStatic
    def post(self, application_id, car_id):
        app = Application.query.get_or_404(application_id)
        car = Car.query.get_or_404(car_id)

        app.cars.append(car)
        db.session.commit()

        response = {
            'application_id': app.application_id,
            'car_id': car.car_id
        }

        return {'data': response}, 200

    # открепить от данной Application объект Car
    # noinspection PyMethodMayBeStatic
    def delete(self, application_id, car_id):
        app = Application.query.get_or_404(application_id)
        car = Car.query.get_or_404(car_id)

        app.cars.remove(car)
        db.session.commit()

        response = {
            'application_id': app.application_id,
            'car_id': car.car_id
        }

        return {'data': response}, 200
