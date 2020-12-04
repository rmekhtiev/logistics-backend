from app.models import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    position = db.Column(db.String(32), nullable=True)
    organization = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(11), nullable=False)

    """ Ссылки на Application """
    application_ship = db.relationship('Application', backref='shipper', uselist=True,
                                       foreign_keys='Application.shipper_id')
    application_receive = db.relationship('Application', backref='receiver', uselist=True,
                                          foreign_keys='Application.receiver_id')

    fields = {
        'last_name': not None,
        'first_name': not None,
        'middle_name': None,
        'position': None,
        'organization': None,
        'phone': not None,
    }

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
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name or ''])
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
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name or ''])
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Contact
    def from_dict(self, data):
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])

    def __repr__(self):
        return "<Contact № {}>".format(self.contact_id)
