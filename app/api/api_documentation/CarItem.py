from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class CarItem:
    """ Car model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'model': {
                'type': 'string',
                'required': True
            },
            'category': {
                'type': "string",
                'required': True
            },
            'weight': {
                'type': "float",
                'required': True
            },
            'volume': {
                'type': 'float',
                'required': True
            }
        }
    }

    resource_fields = {
        'model': fields.String,
        'category': fields.String,
        'weight': fields.Float,
        'volume': fields.Float,
    }
