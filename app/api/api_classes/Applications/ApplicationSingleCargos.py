from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Application, Cargo


# Все грузы у конкретной заявки
from app.api.api_documentation.ApplicationItem import ApplicationItem


class ApplicationSingleCargos(Resource):
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get an application',
        summary="",
        nickname="Applications GET",
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
        cargos = app.cargos.all()
        data = Cargo.to_dict_list(cargos)
        return {'data': data}, 200
