from app.models import db


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

    """ Список контрактов у реквизита многие-ко-одному"""
    contracts = db.relationship('Contract', backref='requisite', lazy='dynamic')

    # Преобразование объекта Requisite в словарь
    def to_dict(self):
        data = {
            'id': self.requisite_id,
            'attributes':
                {
                    'bank_name': self.bank_name,
                    'BIK': self.BIK,
                    'INN': self.INN,
                    'KPP': self.KPP,
                    'KS': self.KS,
                    'RS': self.RS,
                    'bank_account': self.bank_account,
                    'name': self.bank_account + ', ' + self.INN
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
                        'KPP': data.KPP,
                        'KS': data.KS,
                        'RS': data.RS,
                        'bank_account': data.bank_account,
                        'name': data.bank_account + ', ' + data.INN
                    }
            }
            for data in list_data]
        return new_data

    # Извлечение доступных not null данных из словаря в объект типа Requisite
    def from_dict(self, data):
        for field in ['bank_name', 'BIK', 'INN', 'KS', 'RS', 'bank_account']:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])

    def __repr__(self):
        return "<Requisite №: {}>".format(self.requisite_id)
