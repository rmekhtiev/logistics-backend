from app.api.api_classes import Resource
from app.api.api_classes import Application, Driver
from app.api.api_classes import db


# Конкретный водитель у конкретной заявки
class ApplicationSingleDriverSingle(Resource):
    # прикрепить к данной Application объект Driver
    # noinspection PyMethodMayBeStatic
    def post(self, application_id, driver_id):
        app = Application.query.get_or_404(application_id)
        driver = Driver.query.get_or_404(driver_id)

        """ 
                    Или можно вот так добавить:
                    db.session.execute(drivers_applications.insert(),
                           params={"application_id": app.application_id, "driver_id": driver.driver_id})
        """

        app.drivers.append(driver)
        db.session.commit()

        response = {
            'application_id': app.application_id,
            'driver_id': driver.driver_id
        }

        return {'data': response, 'message': "Водитель №{driver} успешно прикреплён к заявке №{app}".format(driver=driver_id, app=application_id)}, 200 # noqa

    # открепить от данной Application объект Driver
    # noinspection PyMethodMayBeStatic
    def delete(self, application_id, driver_id):
        app = Application.query.get_or_404(application_id)
        driver = Driver.query.get_or_404(driver_id)

        app.drivers.remove(driver)
        db.session.commit()

        response = {
            'application_id': app.application_id,
            'driver_id': driver.driver_id
        }

        return {'data': response, 'message': "Водитель №{driver} откреплён от заявки №{app}".format(driver=driver_id, app=application_id)}, 200 # noqa
