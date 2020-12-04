from app.api.api_classes import Resource
from app.api.api_classes import Car, Application


# Послужной список (амортизации) машины
class CarsService(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        applications = []
        for application in car.applications:
            if application.status == 'finished':
                applications.append(application)

        data = Application.to_dict_list(applications)
        return {'data': data}, 200
