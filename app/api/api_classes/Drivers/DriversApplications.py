from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Driver, Application


# Все заявки у конкретного водителя
from app.api.api_documentation.DriverItem import DriverItem


class DriversApplications(Resource):
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a drivers list',
        summary="",
        nickname="Drivers GET",
        responseClass=DriverItem.__name__,
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
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        applications = driver.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
