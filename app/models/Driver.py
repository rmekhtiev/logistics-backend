from app.models import db
from sqlalchemy.dialects.postgresql import ARRAY


class Driver(db.Model):
    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    categories = db.Column(ARRAY(db.String()), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    fields = {
        'last_name': not None,
        'first_name': not None,
        'middle_name': None,
        'categories': not None,
        'phone': not None
    }

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
                    'name': ' '.join([self.last_name, self.first_name, self.middle_name or '']),
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
                        'name': ' '.join([data.last_name, data.first_name, data.middle_name or '']),
                        'phone': data.phone or None
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Driver
    def from_dict(self, data):
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])

    def __repr__(self):
        return "<Driver № {}>".format(self.driver_id)
