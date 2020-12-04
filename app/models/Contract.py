from app.models import db
from datetime import datetime
from sqlalchemy.orm import backref


class Contract(db.Model):
    __tablename__ = 'contracts'

    contract_id = db.Column(db.Integer, primary_key=True)
    conclusion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    cost = db.Column(db.Numeric(10, 2), default=0.0, nullable=False)
    payment_type = db.Column(db.String(32), default='Банковский перевод', nullable=True)

    """ Реквизит """
    requisite_id = db.Column(db.Integer, db.ForeignKey('requisites.requisite_id'), nullable=True)

    """ Заявка """
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=True)
    application = db.relationship('Application', backref=backref('contract', uselist=False), uselist=False)

    """ Клиент """
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=True)

    fields = {
        'conclusion_date': not None,
        'cost': not None,
        'payment_type': None,
        'application_id': None,
        'client_id': None,
        'requisite_id': None
    }

    # Преобразование объекта Contract в словарь
    def to_dict(self):
        data = {
            'id': self.contract_id,
            'attributes':
                {
                    'conclusion_date': str(self.conclusion_date),
                    'cost': float(self.cost),
                    'payment_type': self.payment_type,
                    'application_id': self.application_id,
                    'client_id': self.client_id,
                    'requisite_id': self.requisite_id
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
                        'cost': float(data.cost),
                        'payment_type': data.payment_type,
                        'application_id': data.application_id,
                        'client_id': data.client_id,
                        'requisite_id': data.requisite_id
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
        return "<Contract {}>".format(self.contract_id)
