from app.models import db


class Route(db.Model):
    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(128), nullable=True)
    shipping_address = db.Column(db.String(128), nullable=True)
    distance = db.Column(db.Float, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<Route {} (route number: {}>".format(self.delivery_address, self.route_id)

    fields = {
        'delivery_address': None,
        'shipping_address': None,
        'distance': None,
        'estimated_time': None
    }

    # Преобразование объекта Route в словарь
    def to_dict(self):
        data = {
            'id': self.route_id,
            'attributes':
                {
                    'delivery_address': self.delivery_address,
                    'shipping_address': self.shipping_address,
                    'distance': self.distance,
                    'estimated_time': self.estimated_time,
                    'name': self.shipping_address + ' - ' + self.delivery_address
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
                        'estimated_time': data.estimated_time,
                        'name': data.shipping_address + ' - ' + data.delivery_address
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Route
    def from_dict(self, data):
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])
