from app.api.api_classes import Resource
from app.api.api_classes import Route


# Посмотреть к какой заявке привязан маршрут
class RouteApp(Resource):
    # Получить объект Application from Route
    # noinspection PyMethodMayBeStatic
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        if route.application is not None:
            app = route.application
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This route hasn't got an app"}, 409
