from app.api.api_classes import Resource
from app.api.api_classes import Driver, Application


# Все заявки у конкретного водителя
class DriversApplications(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        applications = driver.applications
        data = Application.to_dict_list(applications)
        return {'data': data}, 200
