from app import db


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

    fields = {
        'passport_number': not None,
        'passport_series': not None,
        'last_name': not None,
        'first_name': not None,
        'middle_name': None,
        'email': None,
        'phone': not None
    }

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
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name or ''])
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
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name or ''])
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Client
    def from_dict(self, data):
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])

    def __repr__(self):
        return "<Client № {}>".format(self.client_id)
