from app import app

from flask_restful import Api

api = Api(app, prefix="/api/v3.0")

from app.api import api_routes  # noqa: E402
