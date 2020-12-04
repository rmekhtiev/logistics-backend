from app import db


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
