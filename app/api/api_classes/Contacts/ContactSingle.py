from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Contact, Client
from app.api.api_classes import db
from app.api.extensions import compare


# Один контакт
class ContactSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('organization', type=str, required=False, location='json')
        self.parser.add_argument('position', type=str, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=False, location='json')
        super(ContactSingle, self).__init__()

    # Получить объект Contact
    # noinspection PyMethodMayBeStatic
    def get(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        data = contact.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Contact
    # noinspection PyMethodMayBeStatic
    def put(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        data = self.parser.parse_args()

        result = compare(contact.to_dict()['attributes'], data)

        for argument in result.keys():
            if not result[argument] and data[argument] is not None:
                if argument == 'phone':
                    # Проверка на правильность телефонного номера
                    if len(data[argument]) > 11 or not data[argument][0] in ['7', '8']:
                        return {'message': "Incorrect phone format"}, 409
                    # Если контакт с таким телефоном уже есть
                    if Contact.query.filter_by(phone=data[argument]).first():
                        return {'message': "Contact with this phone already exists"}, 409
                # Если изменяют что-то из ФИО
                elif argument in ['first_name', 'last_name', 'middle_name']:
                    if Client.query.filter_by(first_name=data[argument], last_name=data[argument],
                                              middle_name=data[argument]).first():  # noqa
                        return {'message': "Client with this full name already exists"}, 409

        contact.from_dict(data)
        db.session.commit()
        return {'data': contact.to_dict(), 'message': "Контакт №{} успешно изменён".format(contact_id)}, 200

    # Удалить объект Contact
    # noinspection PyMethodMayBeStatic
    def delete(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)

        db.session.delete(contact)
        db.session.commit()
        data = contact.to_dict()
        return {'data': data, 'message': "Контакт №{} успешно изменён".format(contact_id)}, 200
