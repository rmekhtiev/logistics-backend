import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'petya'
    DB_URI = 'postgresql+psycopg2://{user}:{password}@{url}/{db}'.format(user='postgres', password='petya',
                                                                         url='localhost:5432', db='logistics')
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
