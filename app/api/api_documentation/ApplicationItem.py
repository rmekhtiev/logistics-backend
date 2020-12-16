from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class ApplicationItem:
    """ Application model """
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64'
        },
        'attributes': {
            'name': {
                'type': 'string',
                'required': True
            },
            'conclusion_date': {
                'type': "datetime",
                'required': False
            },
            'delivery_route': {
                'type': "integer",
                'required': False
            },
            'shipper_id': {
                'type': "integer",
                'required': False
            },
            'receiver_id': {
                'type': "integer",
                'required': False
            },
            'status': {
                'type': "string",
                'required': False,
                'default': "active"
            }
        }
    }

    resource_fields = {
        'name': fields.String,
        'conclusion_date': fields.DateTime(dt_format='rfc822'),
        'delivery_route': fields.Integer,
        'shipper_id': fields.Integer,
        'receiver_id': fields.Integer,
        'status': fields.Boolean(default='active', attribute='super_status')
    }
