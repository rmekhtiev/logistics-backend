from flask_restful import marshal_with

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Application, Contact, Route
from app.api.api_classes import db, datetime
from flask_restful_swagger import swagger
from app.api.api_documentation.ApplicationItem import ApplicationItem


# Список всех заявок
class Applications(Resource):
    """
    Applications describing
    """
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True,
                                 help='application name (description) not provided', location='json')
        self.parser.add_argument('conclusion_date', type=str, required=False,
                                 default=datetime.utcnow, location='json')
        self.parser.add_argument('delivery_route', type=int, required=False, location='json')
        self.parser.add_argument('shipper_id', type=int, required=False, location='json')
        self.parser.add_argument('receiver_id', type=int, required=False, location='json')
        self.parser.add_argument('status', type=str, required=False,
                                 default='active', location='json')
        super(Applications, self).__init__()

    # Выдать список всех объектов типа Application
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get an applications list',
        summary="get all applications",
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
    def get(self):
        applications_list = Application.query.all()
        data = Application.to_dict_list(applications_list)
        return {'data': data}, 200

    # Добавить новый объект типа Application
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create an application',
        summary="",
        nickname="Applications POST",
        responseClass=ApplicationItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": ApplicationItem.properties,
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
                if attribute == 'name':
                    if Application.query.filter_by(name=data[attribute]).first():
                        return {'message': "An application with this name already exist, choose another name"}
                if attribute == 'conclusion_date':
                    if data[attribute] > datetime.utcnow():
                        return {'message': "Provided datetime is bigger than existing {date}".format(date=datetime.utcnow())} # noqa
                if attribute == 'delivery_route':
                    if not Route.query.get(data[attribute]):
                        return {'message': "This route doesn't exist: {route}".format(route=data[attribute])}
                if attribute == 'shipper_id' or attribute == 'receiver_id':
                    if not Contact.query.get(data[attribute]):
                        return {'message': "This contact doesn't exist: {contact}".format(contact=data[attribute])}
                if attribute == 'status':
                    if data[attribute] == 'finished':
                        return {'message': "Cannot create a finished application"}
            else:
                if attribute in ['name']:
                    return {'message': "Field '{name}' cannot be empty".format(name=attribute)}

        application = Application()
        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return {'data': application.to_dict(), 'message': "Заявка успешно создана"}, 201
