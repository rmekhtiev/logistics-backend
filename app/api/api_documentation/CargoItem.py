from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class CargoItem:
    """ Cargo model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'nomenclature': {
                'type': 'string',
                'required': True
            },
            'weight': {
                'type': "float",
                'required': True
            },
            'application_id': {
                'type': "integer",
                'required': False
            }
        }
    }

    resource_fields = {
        'nomenclature': fields.String,
        'weight': fields.Float,
        'application_id': fields.Integer,
    }
