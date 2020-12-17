# AS simple as possible flask google oAuth 2.0
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth, oauth_registry
import requests_oauthlib
import requests
from app import app
# decorator for routes that should be accessible only by logged in users
from app.auth.auth_decorator import login_required

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='976076957713-skc9a5f64996jtgrfi9gfmf53ertr29f.apps.googleusercontent.com',  # os.getenv("GOOGLE_CLIENT_ID"),
    client_secret='f8eikgnkoAi4wNAy4yEuRymX',  # os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/test')
@login_required
def hello_world():
    email = dict(session)['profile']['email']
    return f'Hello, you are logged in as {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/test')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/test')
