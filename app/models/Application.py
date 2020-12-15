from app.models import db
from datetime import datetime
from app.models.cars_apps import cars_applications
from app.models.drivers_apps import drivers_applications


class Application(db.Model):
    __tablename__ = 'applications'

    """ Свои поля """
    application_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(9), default='active', nullable=False)

    """ Маршрут """
    delivery_route = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    route = db.relationship('Route', backref='application', uselist=False)

    """ Поле cargos - все грузы, которое имеет self приложение (Абстракция от SQLAlchemy)"""
    cargos = db.relationship('Cargo', backref='application', lazy='dynamic')

    """ Грузоотправитель """
    shipper_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))

    """ Грузополучатель """
    receiver_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))

    """ Отношение многие-ко-многим с сущностью Cars"""
    cars = db.relationship('Car', secondary=cars_applications, backref='applications', lazy='dynamic')

    """ Отношение многие-ко-многим с сущностью Drivers"""
    drivers = db.relationship('Driver', secondary=drivers_applications, backref='applications', lazy='dynamic')

    def __repr__(self):
        return "<Application {} (app number: {}>".format(self.name, self.application_id)

    fields = {
        'name': not None,
        'conclusion_date': not None,
        'delivery_route': None,
        'shipper_id': None,
        'receiver_id': None,
        'status': not None
    }

    # Преобразование объекта Application в словарь
    def to_dict(self):
        data = {
            'id': self.application_id,
            'attributes':
                {
                    'name': self.name,
                    'conclusion_date': str(self.conclusion_date),
                    'status': self.status,
                    'delivery_route': self.delivery_route,
                    'shipper_id': self.shipper_id,
                    'receiver_id': self.receiver_id,
                }
        }
        return data

    # Преобразование списка объектов Application в словарь
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.application_id,
                'attributes':
                    {
                        'name': data.name,
                        'conclusion_date': str(data.conclusion_date),
                        'status': data.status,
                        'delivery_route': data.delivery_route,
                        'shipper_id': data.shipper_id,
                        'receiver_id': data.receiver_id,
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Application
    def from_dict(self, data):
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])
