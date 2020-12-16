from app import app
from flask_restful import Api
from flask_restful_swagger import swagger

api = Api(app, prefix="/api/v3.0")
api = swagger.docs(api=api, apiVersion="3.0")
from app.api import api_routes  # noqa: E402
