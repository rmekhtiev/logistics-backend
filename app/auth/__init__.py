from app import app

from flask_bcrypt import Bcrypt
from flask_cors import CORS

CORS(app)
bcrypt = Bcrypt(app)

from app.auth import models, views  # noqa: E402