from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Application, Contact, Route
from app.api.api_classes import db
from app.api.extensions import compare


# Одна конкретная заявка
class ApplicationSingle(Resource):
    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=False, location='json')
        self.parser.add_argument('conclusion_date', type=str, required=False, location='json')
        self.parser.add_argument('delivery_route', type=int, required=False, location='json')
        self.parser.add_argument('shipper_id', type=int, required=False, location='json')
        self.parser.add_argument('receiver_id', type=int, required=False, location='json')
        self.parser.add_argument('status', type=str, required=False, location='json')
        super(ApplicationSingle, self).__init__()

    # Получить объект Application
    # noinspection PyMethodMayBeStatic
    def get(self, application_id):
        application = Application.query.get_or_404(application_id)
        data = application.to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Application
    # noinspection PyMethodMayBeStatic
    def put(self, application_id):
        application = Application.query.get_or_404(application_id)
        data = self.parser.parse_args()

        result = compare(application.to_dict()['attributes'], data)

        for attribute in result.keys():
            if not result[attribute]:
                # Если меняют что-то, а заявка уже выполнена
                if application.status == 'finished':
                    return {'message': "Cannot change anything, application is already finished"}, 409
                # Если поле не null
                if data[attribute] is not None:
                    # Если меняют статус
                    if attribute == 'status':
                        if application.status == 'finished':
                            return {'message': "This application is finished. Cannot change anything"}, 409
                    # Если меняют имя
                    if attribute == 'name':
                        if Application.query.filter_by(name=data[attribute]).first():
                            return {'message': "Application with this name already exists"}, 409
                    # Если хотят изменить delivery_route (маршрут)
                    if attribute == 'delivery_route':
                        if not Route.query.get(data[attribute]):
                            return {'message': "This delivery route doesn't exist. Please use a different route"}, 409
                    # Если меняют контактных лиц
                    if attribute == 'shipper_id' or attribute == 'receiver_id':
                        if not Contact.query.get(data[attribute]):
                            return {'message': "This contact doesn't exist. Please use a different one"}, 409
                    # Если меняют дату составления
                    if attribute == 'conclusion_date':
                        return {'message': "Cannot change conclusion date, it is set automatically"}, 409

        application.from_dict(data)
        db.session.add(application)
        db.session.commit()
        return {'data': application.to_dict()}, 201

    # Удалить объект Application
    # noinspection PyMethodMayBeStatic
    def delete(self, application_id):
        application = Application.query.get_or_404(application_id)

        if application.status == 'active':
            return {'message': "This application is active and cannot be deleted until it's finished"}, 409

        db.session.delete(application)
        db.session.commit()
        return {'data': application.to_dict()}, 200
