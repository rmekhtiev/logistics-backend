from app.models import db


""" Смежная таблица многие-ко-многим (applications - drivers) """
drivers_applications = db.Table('drivers_applications',
                                db.Column('driver_id', db.Integer, db.ForeignKey('drivers.driver_id')),
                                db.Column('application_id', db.Integer, db.ForeignKey('applications.application_id')),
                                db.Column('drivers_applications_id', db.Integer, primary_key=True)
                                )
