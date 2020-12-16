from flask_restful_swagger import swagger

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Route, Application
from app.api.api_classes import db
from app.api.api_documentation.RouteItem import RouteItem
from app.api.extensions import compare


# Один маршрут
class RouteSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('delivery_address', type=str, required=False, location='json')
        self.parser.add_argument('shipping_address', type=str, required=False, location='json')
        self.parser.add_argument('distance', type=float, required=False, location='json')
        self.parser.add_argument('estimated_time', type=int, required=False, location='json')
        super(RouteSingle, self).__init__()

    # Получить объект Route
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
        data = route.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Route
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create a route',
        summary="",
        nickname="Routes POST",
        responseClass=RouteItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": RouteItem.properties,
                "required": True
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def put(self, route_id):
        route = Route.query.get_or_404(route_id)
        data = self.parser.parse_args()

        result = compare(route.to_dict()['attributes'], data)

        # Проверка на завершённость заявки при изменении любого поля маршрута
        for argument in result.keys():
            if not result[argument]:
                application = Application.query.filter_by(delivery_route=route_id).first()
                if application and application.status == 'finished':
                    return {'message': "Cannot modify a route, that has a finished application"}, 409
                else:
                    break

        route.from_dict(data)
        db.session.commit()
        return {'data': route.to_dict(), 'message': "Маршрут №{} успешно изменён".format(route_id)}, 200

    # Удалить объект Route
    # noinspection PyMethodMayBeStatic
    def delete(self, route_id):
        route = Route.query.get_or_404(route_id)

        db.session.delete(route)
        db.session.commit()
        data = route.to_dict()
        return {'data': data, 'message': "Маршрут №{} успешно удалён".format(route_id)}, 200
