from app import app

from flask_bcrypt import Bcrypt
from flask_cors import CORS

CORS(app)
bcrypt = Bcrypt(app)

from app.auth.views.bluprint_routes import auth_blueprint  # noqa: E402

app.register_blueprint(auth_blueprint)
