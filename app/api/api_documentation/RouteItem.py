from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class RouteItem:
    """ Route model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'delivery_address': {
                'type': 'string',
                'required': True
            },
            'shipping_address': {
                'type': "string",
                'required': True
            },
            'distance': {
                'type': "float",
                'required': False
            },
            'estimated_time': {
                'type': "integer",
                'required': False
            }
        }
    }

    resource_fields = {
        'delivery_address': fields.String,
        'shipping_address': fields.String,
        'distance': fields.Float,
        'estimated_time': fields.Integer
    }