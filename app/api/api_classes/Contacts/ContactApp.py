from app.api.api_classes import Resource
from app.api.api_classes import Contact


# Информация о том какой груз (заявку) ожидает контакт
class ContactApp(Resource):
    # Получить объект Application from Contact
    # noinspection PyMethodMayBeStatic
    def get(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)

        # Проверяем есть ли у контакта привязка к заявке
        if contact.application_receive is not None:
            app = contact.application_receive
            return {'data': app.to_dict()}, 200
        if contact.application_shipp is not None:
            app = contact.application_shipp
            return {'data': app.to_dict()}, 200
        else:
            return {'message': "This contact isn't linked to an app"}, 409
