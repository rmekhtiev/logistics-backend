from flask_restful_swagger import swagger

from app.api.api_classes import Resource
from app.api.api_classes import Route


# Посмотреть к какой заявке привязан маршрут
from app.api.api_documentation.RouteItem import RouteItem


class RouteApp(Resource):
    # Получить объект Application from Route
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a routes list',
        summary="",
        nickname="Routes GET",
        responseClass=RouteItem.__name__,
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
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        if route.application is not None:
            app = route.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This route hasn't got an app"}, 409
