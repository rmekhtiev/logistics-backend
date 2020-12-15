from app.api.api_classes import Resource
from app.api.api_classes import Application, Car


# Все машины у конкретной заявки
class ApplicationSingleCars(Resource):
    # Выдать список всех объектов Car у данного Application
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cars = app.cars
        data = Car.to_dict_list(cars)
        return {'data': data}, 200
