from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Car, Application


# Все заявки у конкретной машины
from app.api.api_documentation.CarItem import CarItem


class CarsApplications(Resource):
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a cars list',
        summary="",
        nickname="Cars GET",
        responseClass=CarItem.__name__,
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Success"
            },
            {
                "code": 404,
                "message": "Not Found"
            }
        ]
    )
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        applications = car.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
