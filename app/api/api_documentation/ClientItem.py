from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class ClientItem:
    """ Client model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'passport_number': {
                'type': 'integer',
                'required': True
            },
            'passport_series': {
                'type': "integer",
                'required': True
            },
            'last_name': {
                'type': "string",
                'required': True
            },
            'first_name': {
                'type': "string",
                'required': True
            },
            'middle_name': {
                'type': "string",
                'required': False
            },
            'email': {
                'type': "string",
                'required': False
            },
            'phone': {
                'type': "string",
                'required': True
            }
        }
    }

    resource_fields = {
        'passport_number': fields.Integer,
        'passport_series': fields.Integer,
        'last_name': fields.String,
        'first_name': fields.String,
        'middle_name': fields.String,
        'email': fields.String,
        'phone': fields.String
    }
