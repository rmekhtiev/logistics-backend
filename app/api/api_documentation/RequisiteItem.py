from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class RequisiteItem:
    """ Requisite model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'bank_name': {
                'type': 'string',
                'required': True
            },
            'bank_account': {
                'type': "string",
                'required': True
            },
            'BIK': {
                'type': "string",
                'required': True
            },
            'INN': {
                'type': "string",
                'required': True
            },
            'KPP': {
                'type': "string",
                'required': True
            },
            'KS': {
                'type': "string",
                'required': True
            },
            'RS': {
                'type': "string",
                'required': True
            }
        }
    }

    resource_fields = {
        'bank_name': fields.String,
        'bank_account': fields.String,
        'BIK': fields.String,
        'INN': fields.String,
        'KPP': fields.String,
        'KS': fields.String,
        'RS': fields.String
    }