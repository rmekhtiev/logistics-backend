from authlib.integrations.flask_client import OAuth
from flask import url_for, redirect, session
from app import app

app.secret_key = 'random secret'

# oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='873662315470-cl72tdjasmlnhobsadr8sbulvur16i5h.apps.googleusercontent.com',
    client_secret='4AgEzUZOYTDMsiqOSglQpvm9',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    acess_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='http://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def hello():
    email = dict(session).get('email', None)
    return f'Hello, {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
