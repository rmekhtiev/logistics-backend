from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class ContactItem:
    """ Contact model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'last_name': {
                'type': 'string',
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
            'organization': {
                'type': "string",
                'required': False
            },
            'position': {
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
        'last_name': fields.String,
        'first_name': fields.String,
        'middle_name': fields.String,
        'organization': fields.String,
        'position': fields.String,
        'phone': fields.String
    }
