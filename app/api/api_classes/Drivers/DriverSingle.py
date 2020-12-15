from app.api.api_classes import Resource, reqparse
from app.api.api_classes import Driver
from app.api.api_classes import db
from app.api.extensions import compare


# Один водитель
class DriverSingle(Resource):

    # Настройка запроса request и его полей
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', type=str, required=False, location='json')
        self.parser.add_argument('first_name', type=str, required=False, location='json')
        self.parser.add_argument('middle_name', type=str, required=False, location='json')
        self.parser.add_argument('categories', type=list, required=False, location='json')
        self.parser.add_argument('phone', type=str, required=False, location='json')
        super(DriverSingle, self).__init__()

    # Получить объект Driver
    # noinspection PyMethodMayBeStatic
    def get(self, driver_id):
        data = Driver.query.get_or_404(driver_id).to_dict()
        return {'data': data}, 200

    # Внести изменения в объект Driver
    # noinspection PyMethodMayBeStatic
    def put(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        data = self.parser.parse_args()

        result = compare(driver.to_dict()['attributes'], data)

        for attribute in result.keys():
            if not result[attribute] and data[attribute] is not None:
                # Если изменяют номер телефона
                if attribute == 'phone':
                    # Проверка на правильность телефонного номера
                    if len(data[attribute]) > 11 or not data[attribute][0] in ['7', '8']:
                        return {'message': "Incorrect phone format"}, 409
                    # Если контакт с таким телефоном уже есть
                    if Driver.query.filter_by(phone=data[attribute]).first():
                        return {'message': "Driver with this phone already exists"}, 409
                # Если изменяют что-то из ФИО
                elif attribute in ['first_name', 'last_name', 'middle_name']:
                    if Driver.query.filter_by(first_name=data[attribute], last_name=data[attribute],
                                              middle_name=data[attribute]).first():  # noqa
                        return {'message': "Driver with this full name already exists"}, 409

        driver.from_dict(data)
        db.session.commit()
        return {'data': driver.to_dict(), 'message': "Водитель №{} успешно изменён".format(driver_id)}, 200

    # Удалить объект Driver
    # noinspection PyMethodMayBeStatic
    def delete(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)

        # Если у водитель есть активный заказ
        applications = driver.applications
        for application in applications:
            if application.status == 'active':
                return {'message': "This driver has an order and cannot be deleted (is not free)"}, 409

        db.session.delete(driver)
        db.session.commit()
        return {'data': driver.to_dict(), 'message': "Водитель №{} успешно удалён".format(driver_id)}, 200
