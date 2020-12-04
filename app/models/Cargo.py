from app.models import db


class Cargo(db.Model):
    __tablename__ = 'cargos'

    """ Свои поля """
    cargo_id = db.Column(db.Integer, primary_key=True)
    nomenclature = db.Column(db.String(64), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)

    # Словарь полей для корректного использования setattr
    fields = {'nomenclature': not None, 'weight': not None, 'application_id': None}

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
        for field in self.fields:
            # Пихаем значение, если оно не None и относиться к нашим полям, либо если оно None и поле может быть таким
            if field in data:
                if data[field] is not None:
                    setattr(self, field, data[field])
                elif data[field] is None and self.fields[field] is None:
                    setattr(self, field, data[field])

    def __repr__(self):
        return "<Order № {} (order number: {}>".format(self.nomenclature, self.cargo_id)
