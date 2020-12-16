from flask_restful_swagger import swagger

from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Contact
from app.api.api_classes import db


# Все контакты
from app.api.api_documentation.ContactItem import ContactItem


class Contacts(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=True,
                                 help='last name not provided', location='json')
        self.parser.add_argument('first_name', type=str, required=True,
                                 help='first name not provided', location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('organization', type=str, required=False, location='json')
        self.parser.add_argument('position', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=True,
                                 help='phone not provided', location='json')
        super(Contacts, self).__init__()

    # Выдать список всех объектов Contact
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='get a contacts list',
        summary="",
        nickname="Contacts GET",
        responseClass=ContactItem.__name__,
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
        contacts_list = Contact.query.all()
        data = Contact.to_dict_list(contacts_list)
        return {'data': data}, 200

    # Создать новый объект Contact
    # noinspection PyMethodMayBeStatic
    @swagger.operation(
        notes='create a contact',
        summary="",
        nickname="Contacts POST",
        responseClass=ContactItem.__name__,
        parameters=[
            {
                "allowMultiple": False,
                "dataType": "ApplicationItem",
                "description": "An Application item",
                "name": "body",
                "paramType": "body",
                "properties": ContactItem.properties,
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
                if attribute in ['last_name', 'first_name', 'middle_name', 'position']:
                    if len(data[attribute]) > 32:
                        return {'message': "{} length cannot be bigger than 32".format(attribute)}, 409
                if attribute == 'phone':
                    # Проверка на правильность телефонного номера
                    if len(data['phone']) > 11 or not data['phone'][0] == '7':
                        return {'message': "Incorrect phone format"}, 409
                    # Если контакт с таким телефоном уже есть
                    if Contact.query.filter_by(phone=data['phone']).first():
                        return {'message': "Contact with this phone already exists"}, 409
                if attribute == 'organization':
                    if len(data[attribute]) > 64:
                        return {'message': "Organization length cannot be bigger than 64"}, 409
            else:
                if attribute in ['last_name', 'first_name', 'phone']:
                    return {'message': "Field {} cannot be null".format(attribute)}, 409

        contact = Contact()
        contact.from_dict(data)
        db.session.add(contact)
        db.session.commit()
        data = contact.to_dict()
        return {'data': data, 'message': "Контакт успешно создан"}, 201
