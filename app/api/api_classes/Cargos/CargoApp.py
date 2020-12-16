from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Cargo


# Посмотреть к какой заявке привязан груз
from app.api.api_documentation.ApplicationItem import ApplicationItem
from app.api.api_documentation.CargoItem import CargoItem


class CargoApp(Resource):
    # Получить объект Application from Cargo
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a cargos list',
        summary="",
        nickname="Cargos GET",
        responseClass=CargoItem.__name__,
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
    def get(self, cargo_id):
        cargo = Cargo.query.get_or_404(cargo_id)
        if cargo.application is not None:
            app = cargo.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This cargo isn't in an app"}, 409
