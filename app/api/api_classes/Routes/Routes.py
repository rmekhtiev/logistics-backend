from flask_restful_swagger import swagger

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Route
from app.api.api_classes import db


# Список маршрутов
from app.api.api_documentation.RouteItem import RouteItem


class Routes(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('delivery_address', type=str, required=True,
                                 help='delivery_address not provided', location='json')
        self.parser.add_argument('shipping_address', type=str, required=True,
                                 help='shipping_address not provided', location='json')
        self.parser.add_argument('distance', type=float, required=False, location='json')
        self.parser.add_argument('estimated_time', type=int, required=False, location='json')
        super(Routes, self).__init__()

    # Выдать список всех объектов Route
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
    def get(self):
        routes_list = Route.query.all()
        data = Route.to_dict_list(routes_list)
        return {'data': data}, 200

    # Создать новый объект Route
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
    def post(self):
        data = self.parser.parse_args()

        # Здесь проверку на что-либо делать незачем

        route = Route()
        route.from_dict(data)
        db.session.add(route)
        db.session.commit()
        data = route.to_dict()
        return {'data': data, 'message': "Маршрут успешно создан"}, 201
