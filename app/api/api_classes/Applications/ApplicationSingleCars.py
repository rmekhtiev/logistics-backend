from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Application, Car


# Все машины у конкретной заявки
from app.api.api_documentation.ApplicationItem import ApplicationItem


class ApplicationSingleCars(Resource):
    # Выдать список всех объектов Car у данного Application
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get an application',
        summary="",
        nickname="ApplicationSingleCars GET",
        responseClass=ApplicationItem.__name__,
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
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cars = app.cars
        data = Car.to_dict_list(cars)
        return {'data': data}, 200
