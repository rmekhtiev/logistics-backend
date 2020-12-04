from app.api.api_classes import Resource
from app.api.api_classes import Application, Cargo


# Все грузы у конкретной заявки
class ApplicationSingleCargos(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        app = Application.query.get_or_404(application_id)
        cargos = app.cargos.all()
        data = Cargo.to_dict_list(cargos)
        return {'data': data}, 200
