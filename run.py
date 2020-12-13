from app import app

app.run(debug=False, host='0.0.0.0')

"""
from flask_cli import FlaskGroup

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
"""