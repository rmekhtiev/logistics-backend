from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, BOOLEAN, ARRAY

""" Смежная таблица многие-ко-многим (applications - cars) """
cars_applications = db.Table('cars_applications',
                             db.Column('car_id', db.Integer, db.ForeignKey('cars.car_id')),
                             db.Column('application_id', db.Integer, db.ForeignKey('applications.application_id')),
                             db.Column('cars_applications_id', db.Integer, primary_key=True)
                             )

""" Смежная таблица многие-ко-многим (applications - drivers) """
drivers_applications = db.Table('drivers_applications',
                                db.Column('driver_id', db.Integer, db.ForeignKey('drivers.driver_id')),
                                db.Column('application_id', db.Integer, db.ForeignKey('applications.application_id')),
                                db.Column('drivers_applications_id', db.Integer, primary_key=True)
                                )


class Cargo(db.Model):
    __tablename__ = 'cargos'

    """ Свои поля """
    cargo_id = db.Column(db.Integer, primary_key=True)
    nomenclature = db.Column(db.String(64), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'))

    def __repr__(self):
        return "<Order {} (order number: {}>".format(self.nomenclature, self.cargo_id)

    # Преобразование списка объектов в словарь
    @staticmethod
    def to_dict_list(list_data):
        data = [
            {
                'id': data.cargo_id,
                'nomenclature': data.nomenclature,
                'weight': data.weight,
            }
            for data in list_data]
        return data


class Application(db.Model):
    __tablename__ = 'applications'

    """ Свои поля """
    application_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    is_finished = db.Column(db.Boolean, default=False)

    """ Маршрут """
    delivery_route = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    route = db.relationship('Route', backref='application', uselist=False)

    """ Оплата """
    payment_detail = db.Column(db.Integer, db.ForeignKey('payments.payment_id'))
    payment = db.relationship('Payment', backref='application', uselist=False)

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

    # Преобразование объекта в словарь
    def to_dict(self, JOIN):
        if JOIN:
            data = {
                'id': self.application_id,
                'name': self.name,
                'conclusion date': self.conclusion_date,
                'route': Route.query.get(self.delivery_route).to_dict(),
                'payment': Payment.query.get(self.payment_detail).to_dict()
            }
        else:
            data = {
                'id': self.application_id,
                'name': self.name,
                'conclusion date': self.conclusion_date,
                'route': self.delivery_route,
                'payment': self.payment_detail
            }
        return data

    # Преобразование списка объектов в словарь
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.application_id,
                'name': data.name,
                'conclusion date': data.conclusion_date,
                'route': data.delivery_route,
                'payment': data.payment_detail
            }
            for data in list_data]
        return new_data

    # Извлечение данных в объект типа Application
    def from_dict(self, data):
        for field in ['name', 'conclusion_date', 'delivery_route', 'payment_detail']:
            if field in data:
                setattr(self, field, data[field])


class Route(db.Model):
    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(128), nullable=False)
    shipping_address = db.Column(db.String(128), nullable=False)
    distance = db.Column(db.Float, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)

    # def __init__(self, delivery_address, shipping_address):
    #     self.delivery_address = delivery_address
    #     self.shipping_address = shipping_address

    def __repr__(self):
        return "<Route {} (route number: {}>".format(self.delivery_address, self.route_id)

    def to_dict(self):
        data = {
            'id': self.route_id,
            'delivery_address': self.delivery_address,
            'shipping_address': self.shipping_address,
            'distance': self.distance,
            'estimated_time': self.estimated_time
        }
        return data


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.String(32), nullable=False)
    short_change = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return "<Payment {}>".format(self.payment_id)

    def to_dict(self):
        data = {
            'id': self.payment_id,
            'cost': float(self.cost),
            'payment_type': self.payment_type,
            'short_change': self.short_change
        }
        return data


class Contract(db.Model):
    __tablename__ = 'contracts'

    contract_id = db.Column(db.Integer, primary_key=True)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)

    """Реквизиты"""
    bank_name = db.Column(db.String(64), nullable=False)
    BIK = db.Column(db.String(9), nullable=False)
    INN = db.Column(db.String(10), nullable=False)
    KPP = db.Column(db.String(9), nullable=False)
    KS = db.Column(db.String(20), nullable=False)
    bank_account = db.Column(db.String(20), nullable=False)

    """Заявка"""
    application_num = db.Column(db.Integer, db.ForeignKey('applications.application_id'))
    application = db.relationship('Application', backref='contract', uselist=False)

    """Клиент"""
    client_detail = db.Column(db.Integer, db.ForeignKey('clients.client_id'))

    def __repr__(self):
        return "<Contract {}>".format(self.contract_id)


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    passport_id = db.Column(db.Integer, nullable=False)
    passport_series = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(11))

    """ Список контрактов у клиента многие-ко-многим """
    contracts = db.relationship('Contract', backref='client', lazy='dynamic')

    def __repr__(self):
        return "<Client {}>".format(self.client_id)


class Driver(db.Model):
    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    categories = db.Column(ARRAY(db.String()), nullable=True)
    is_free = db.Column(db.Boolean, default=True, nullable=False)

    # Преобразование объекта Driver в словарь
    def to_dict(self):
        data = {
            'driver_id': self.driver_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name or None,
            'categories': self.categories or None,
            'is_free': self.is_free
        }
        return data

    # Преобразование списка объектов типа Driver в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'driver_id': data.driver_id,
                'last_name': data.first_name,
                'first_name': data.last_name,
                'middle_name': data.middle_name or None,
                'categories': data.categories or None,
                'is_free': data.is_free
            }
            for data in list_data]
        return new_data

    # Извлечение данных из словаря в объект типа Driver
    def from_dict(self, data):
        for field in ['last_name', 'first_name', 'middle_name', 'categories']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Driver {}>".format(self.driver_id)


class Contact(db.Model):
    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32))
    position = db.Column(db.String(32))
    organization = db.Column(db.String(64))
    telephone = db.Column(db.String(11))

    """ Ссылки на Application """
    application_ship = db.relationship('Application', backref='shipper', uselist=False,
                                       foreign_keys='Application.shipper_id')
    application_receive = db.relationship('Application', backref='receiver', uselist=False,
                                          foreign_keys='Application.receiver_id')

    def __repr__(self):
        return "<Contact №: {}>".format(self.contact_id)


class Car(db.Model):
    __tablename__ = 'cars'

    car_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    model = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(1), nullable=False)
    is_free = db.Column(db.Boolean, default=True, nullable=False)

    # Преобразование объекта Car в словарь
    def to_dict(self):
        data = {
            'car_id': self.car_id,
            'model': self.model,
            'category': self.category,
            'weight': self.weight,
            'volume': self.volume,
            'is_free': self.is_free
        }
        return data

    # Преобразование списка объектов типа Car в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'car_id': data.car_id,
                'model': data.model,
                'category': data.category,
                'weight': data.weight,
                'volume': data.volume,
                'is_free': data.is_free
            }
            for data in list_data]
        return new_data

    # Извлечение данных из словаря в объект типа Car
    def from_dict(self, data):
        for field in ['model', 'category', 'weight', 'volume']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Car №: {}>".format(self.car_id)
