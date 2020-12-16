from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Application, Car
from app.api.api_classes import db


# Конкретная машина у конкретной заявки
from app.api.api_documentation.ApplicationItem import ApplicationItem


class ApplicationSingleCarSingle(Resource):
    # прикрепить к данной Application объект Car
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create an application',
        summary="",
        nickname="ApplicationSingleCarSingle POST",
        responseClass=ApplicationItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": ApplicationItem.properties,
                "required": True
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def post(self, application_id, car_id):
        app = Application.query.get_or_404(application_id)
        car = Car.query.get_or_404(car_id)

        app.cars.append(car)
        db.session.commit()

        response = {
            'application_id': app.application_id,
            'car_id': car.car_id
        }

        return {'data': response, 'message': "Машина №{car} успешно прикреплена к заявке №{app}".format(car=car_id, app=application_id)}, 200 # noqa

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

        return {'data': response, 'message': "Машина №{car} успешно откреплена от заявки №{app}".format(car=car_id, app=application_id)}, 200 # noqa
