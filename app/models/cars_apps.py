from app import db


""" Смежная таблица многие-ко-многим (applications - cars) """
cars_applications = db.Table('cars_applications',
                             db.Column('car_id', db.Integer, db.ForeignKey('cars.car_id')),
                             db.Column('application_id', db.Integer, db.ForeignKey('applications.application_id')),
                             db.Column('cars_applications_id', db.Integer, primary_key=True)
                             )
