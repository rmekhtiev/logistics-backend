from app.api.api_classes import Resource
from app.api.api_classes import Application, Driver


# Все водители у конкретной заявки
class ApplicationSingleDrivers(Resource):
    # Выдать список всех объектов Driver
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        drivers = app.drivers.all()
        data = Driver.to_dict_list(drivers)
        return {'data': data}, 200
