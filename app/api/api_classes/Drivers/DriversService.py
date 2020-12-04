from app.api.api_classes import Resource
from app.api.api_classes import Driver, Application


# Послужной список водителя
class DriversService(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        applications = []
        for application in driver.applications:
            if application.status == 'finished':
                applications.append(application)
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
