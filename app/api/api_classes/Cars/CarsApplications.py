from app.api.api_classes import Resource
from app.api.api_classes import Car, Application


# Все заявки у конкретной машины
class CarsApplications(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        applications = car.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
