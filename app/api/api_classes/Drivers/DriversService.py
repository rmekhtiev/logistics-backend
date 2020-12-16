from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Driver, Application


# Послужной список водителя
from app.api.api_documentation.DriverItem import DriverItem


class DriversService(Resource):
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
        applications = []
        for application in driver.applications:
            if application.status == 'finished':
                applications.append(application)
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
