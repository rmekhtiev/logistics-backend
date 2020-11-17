from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

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

    # Преобразование объекта Application в словарь
    def to_dict(self):
        data = {
            'id': self.cargo_id,
            'attributes':
                {
                    'nomenclature': self.nomenclature,
                    'weight': self.weight,
                    'application_id': self.application_id
                }
        }
        return data

    # Преобразование списка объектов Cargo в словарь
    @staticmethod
    def to_dict_list(list_data):
        data = [
            {
                'id': data.cargo_id,
                'attributes':
                    {
                        'nomenclature': data.nomenclature,
                        'weight': data.weight,
                        'application_id': data.application_id
                    }
            }
            for data in list_data]
        return data

    # Извлечение доступных not null данных из словаря в объект типа Application
    def from_dict(self, data):
        for field in ['nomenclature', 'weight', 'application_id']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Order № {} (order number: {}>".format(self.nomenclature, self.cargo_id)


class Application(db.Model):
    __tablename__ = 'applications'

    """ Свои поля """
    application_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(9), default='active', nullable=True)

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
        for field in ['name', 'conclusion_date', 'delivery_route', 'shipper_id', 'receiver_id', 'status']:
            if field in data and data[field] is not None:
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

    # Преобразование объекта Route в словарь
    def to_dict(self):
        data = {
            'id': self.route_id,
            'attributes':
                {
                    'delivery_address': self.delivery_address,
                    'shipping_address': self.shipping_address,
                    'distance': self.distance,
                    'estimated_time': self.estimated_time
                }
        }
        return data

    # Преобразование списка объектов типа Route в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.route_id,
                'attributes':
                    {
                        'delivery_address': data.delivery_address,
                        'shipping_address': data.shipping_address,
                        'distance': data.distance,
                        'estimated_time': data.estimated_time
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Route
    def from_dict(self, data):
        for field in ['delivery_address', 'shipping_address', 'distance', 'estimated_time']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])


class Contract(db.Model):
    __tablename__ = 'contracts'

    contract_id = db.Column(db.Integer, primary_key=True)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.String(32), default='банковский перевод', nullable=True)

    """Реквизиты"""
    requisite = db.relationship('Requisite', backref='contracts', lazy='dynamic')

    """Заявка"""
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'))
    application = db.relationship('Application', backref='contract', uselist=False)

    """Клиент"""
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))

    # Преобразование объекта Contract в словарь
    def to_dict(self):
        data = {
            'id': self.contract_id,
            'attributes':
                {
                    'conclusion_date': str(self.conclusion_date),
                    'cost': str(self.cost),
                    'payment_type': self.payment_type,
                    'application_id': self.application_id,
                    'client_id': self.client_id
                }
        }
        return data

    # Преобразование списка объектов типа Client в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.contract_id,
                'attributes':
                    {
                        'conclusion_date': str(data.conclusion_date),
                        'cost': str(data.cost),
                        'payment_type': data.payment_type,
                        'application_id': data.application_id,
                        'client_id': data.client_id
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Client
    def from_dict(self, data):
        for field in ['conclusion_date', 'cost', 'payment_type', 'application_id', 'client_id']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Contract {}>".format(self.contract_id)


class Requisite(db.Model):
    __tablename__ = 'requisites'

    requisite_id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(64), nullable=False)
    BIK = db.Column(db.String(9), nullable=False)
    INN = db.Column(db.String(10), nullable=False)
    KPP = db.Column(db.String(9), nullable=False)
    KS = db.Column(db.String(20), nullable=False)
    RS = db.Column(db.String(20), nullable=False)
    bank_account = db.Column(db.String(20), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.contract_id'))

    # Преобразование объекта Requisite в словарь
    def to_dict(self):
        data = {
            'id': self.requisite_id,
            'attributes':
                {
                    'bank_name': self.bank_name,
                    'BIK': self.BIK,
                    'INN': self.INN,
                    'KS': self.KS,
                    'RS': self.RS,
                    'bank_account': self.bank_account,
                    'contract_id': self.contract_id
                }
        }
        return data

    # Преобразование списка объектов типа Requisite в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.requisite_id,
                'attributes':
                    {
                        'bank_name': data.bank_name,
                        'BIK': data.BIK,
                        'INN': data.INN,
                        'KS': data.KS,
                        'RS': data.RS,
                        'bank_account': data.bank_account,
                        'contract_id': data.contract_id
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Requisite
    def from_dict(self, data):
        for field in ['bank_name', 'BIK', 'INN', 'KS', 'RS', 'bank_account', 'contract_id']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Requisite №: {}>".format(self.requisite_id)


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.Integer, nullable=False)
    passport_series = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(11), nullable=False)

    """ Список контрактов у клиента многие-ко-одному """
    contracts = db.relationship('Contract', backref='client', lazy='dynamic')

    # Преобразование объекта Client в словарь
    def to_dict(self):
        data = {
            'id': self.client_id,
            'attributes':
                {
                    'passport_number': self.passport_number,
                    'passport_series': self.passport_series,
                    'last_name': self.last_name,
                    'first_name': self.first_name,
                    'middle_name': self.middle_name or None,
                    'email': self.email or None,
                    'phone': self.phone,
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name])
                }
        }
        return data

    # Преобразование списка объектов типа Client в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.client_id,
                'attributes':
                    {
                        'passport_number': data.passport_number,
                        'passport_series': data.passport_series,
                        'last_name': data.last_name,
                        'first_name': data.first_name,
                        'middle_name': data.middle_name or None,
                        'email': data.email or None,
                        'phone': data.phone,
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name])
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Client
    def from_dict(self, data):
        for field in ['passport_number', 'passport_series', 'last_name', 'first_name', 'middle_name', 'email', 'phone']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Client № {}>".format(self.client_id)


class Driver(db.Model):
    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    categories = db.Column(ARRAY(db.String()), nullable=True)
    phone = db.Column(db.String(11), nullable=True)

    # Преобразование объекта Driver в словарь
    def to_dict(self):
        data = {
            'id': self.driver_id,
            'attributes':
                {
                    'last_name': self.last_name,
                    'first_name': self.first_name,
                    'middle_name': self.middle_name or None,
                    'categories': self.categories or None,
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name]),
                    'phone': self.phone or None
                }
        }
        return data

    # Преобразование списка объектов типа Driver в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.driver_id,
                'attributes':
                    {
                        'last_name': data.last_name,
                        'first_name': data.first_name,
                        'middle_name': data.middle_name or None,
                        'categories': data.categories or None,
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name]),
                        'phone': data.phone or None
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Driver
    def from_dict(self, data):
        for field in ['last_name', 'first_name', 'middle_name', 'categories', 'phone']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Driver № {}>".format(self.driver_id)


class Contact(db.Model):
    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    position = db.Column(db.String(32), nullable=True)
    organization = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(11), nullable=True)

    """ Ссылки на Application """
    application_ship = db.relationship('Application', backref='shipper', uselist=False,
                                       foreign_keys='Application.shipper_id')
    application_receive = db.relationship('Application', backref='receiver', uselist=False,
                                          foreign_keys='Application.receiver_id')

    # Преобразование объекта Contact в словарь
    def to_dict(self):
        data = {
            'id': self.contact_id,
            'attributes':
                {
                    'last_name': self.last_name,
                    'first_name': self.first_name,
                    'middle_name': self.middle_name or None,
                    'position': self.position or None,
                    'organization': self.organization or None,
                    'phone': self.phone,
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name])
                }
        }
        return data

    # Преобразование списка объектов типа Contact в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.contact_id,
                'attributes':
                    {
                        'last_name': data.last_name,
                        'first_name': data.first_name,
                        'middle_name': data.middle_name or None,
                        'position': data.position or None,
                        'organization': data.organization or None,
                        'phone': data.phone,
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name])
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Contact
    def from_dict(self, data):
        for field in ['last_name', 'first_name', 'middle_name', 'position', 'organization', 'phone']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Contact № {}>".format(self.contact_id)


class Car(db.Model):
    __tablename__ = 'cars'

    car_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    model = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(1), nullable=False)

    # Преобразование объекта Car в словарь
    def to_dict(self):
        data = {
            'id': self.car_id,
            'attributes':
                {
                    'model': self.model,
                    'category': self.category,
                    'weight': self.weight,
                    'volume': self.volume
                }
        }
        return data

    # Преобразование списка объектов типа Car в список словарей
    @staticmethod
    def to_dict_list(list_data):
        new_data = [
            {
                'id': data.car_id,
                'attributes':
                    {
                        'model': data.model,
                        'category': data.category,
                        'weight': data.weight,
                        'volume': data.volume
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Car
    def from_dict(self, data):
        for field in ['model', 'category', 'weight', 'volume']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Car № {}>".format(self.car_id)
