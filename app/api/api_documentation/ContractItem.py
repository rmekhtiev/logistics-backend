from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class ContractItem:
    """ Contract model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'conclusion_date': {
                'type': 'string',
                'required': False
            },
            'cost': {
                'type': "float",
                'required': True
            },
            'client_id': {
                'type': "integer",
                'required': False
            },
            'payment_type': {
                'type': "string",
                'required': False
            },
            'application_id': {
                'type': "integer",
                'required': False
            },
            'requisite_id': {
                'type': "integer",
                'required': False
            }
        }
    }

    resource_fields = {
        'conclusion_date': fields.String,
        'cost': fields.Float,
        'client_id': fields.Integer,
        'payment_type': fields.String,
        'application_id': fields.Integer,
        'requisite_id': fields.Integer
    }
