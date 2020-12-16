from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Application, Driver


# Все водители у конкретной заявки
from app.api.api_documentation.ApplicationItem import ApplicationItem


class ApplicationSingleDrivers(Resource):
    # Выдать список всех объектов Driver
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get an application',
        summary="",
        nickname="ApplicationSingleDrivers GET",
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
        drivers = app.drivers.all()
        data = Driver.to_dict_list(drivers)
        return {'data': data}, 200
