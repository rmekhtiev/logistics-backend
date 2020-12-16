from flask_restful_swagger import swagger

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Driver
from app.api.api_classes import db


# Все водители
from app.api.api_documentation.DriverItem import DriverItem


class Drivers(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=True,
                                 help='last name not provided', location='json')
        self.parser.add_argument('first_name', type=str, required=True,
                                 help='first name nor provided', location='json')
        self.parser.add_argument('middle_name', type=str, required=False,
                                 default=None, location='json')
        self.parser.add_argument('categories', type=list, required=True,
                                 help='categories not provided', location='json')
        self.parser.add_argument('phone', type=str, required=True,
                                 help='drivers phone not provided', location='json')
        super(Drivers, self).__init__()

    # Выдать список всех объектов Driver
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a drivers list',
        summary="",
        nickname="Drivers GET",
        responseClass=DriverItem.__name__,
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
        drivers_list = Driver.query.all()
        data = Driver.to_dict_list(drivers_list)
        return {'data': data}, 200

    # Создать новый объект Driver
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create a driver',
        summary="",
        nickname="Drivers POST",
        responseClass=DriverItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": DriverItem.properties,
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

        for attribute in data.keys():
            if data[attribute] is not None:
                if attribute in ['last_name', 'first_name', 'middle_name']:
                    if len(data[attribute]) > 32:
                        return {'message': "{} length cannot be bigger than 32".format(attribute)}, 409
                    if Driver.query.filter_by(last_name=data['last_name'],
                                              first_name=data['first_name'],
                                              middle_name=data['middle_name']).first():
                        return {'message': "Driver with this full name already exists"}, 409
                if attribute == 'phone':
                    # Проверка на правильность телефонного номера
                    if len(data['phone']) > 11 or not data['phone'][0] == '7':
                        return {'message': "Incorrect phone format"}, 409
                    # Если водитель с таким номером телефона уже есть
                    if Driver.query.filter_by(phone=data['phone']).first():
                        return {'message': "Driver with this phone already exists"}, 409
            else:
                if attribute in ['last_name', 'first_name', 'phone']:
                    return {'message': "Field {} cannot be null".format(attribute)}, 409

        driver = Driver()
        driver.from_dict(data)
        db.session.add(driver)
        db.session.commit()
        return {'data': driver.to_dict(), 'message': "Водитель успешно создан"}, 201
