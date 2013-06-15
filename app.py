from flask import (Flask, redirect, url_for, session, render_template,
                   request, make_response)
from flask.ext.login import (LoginManager, login_user, logout_user, login_required,
                             current_user)
from flask.ext.oauth import OAuth
from json import dumps, loads
import requests
import os

from orm import User

app = Flask(__name__)

# import config from $APP_CONFIG file

app.config.from_envvar('APP_CONFIG') 
app.secret_key = app.config['SECRET_KEY']

# google oauth2 setup

oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params= {'scope': 'https://www.googleapis.com/auth/userinfo.email \
                          https://www.googleapis.com/auth/userinfo.profile',
                                                 'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=app.config['GOOGLE_CLIENT_ID'],
                          consumer_secret=app.config['GOOGLE_CLIENT_SECRET'])
# login manager

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)    

# routes
 
@app.route('/')
def index():
    return current_user.name #render_template('index.html')

@app.route('/login/google')
def login_google():
    session['next'] = request.args.get('next') or request.referrer or None
    callback=url_for('google_callback', _external=True)    
    return google.authorize(callback=callback)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def google_callback(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    if access_token:
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                         headers={'Authorization': 'OAuth ' + access_token})
        if r.ok:
            data = loads(r.text)
            oauth_id = data['id']
            user = User.load(oauth_id) or User.add(**data)
            login_user(user)
            next_url = session.get('next') or url_for('index')
            return redirect(next_url)
    return redirect(url_for('login')) 

@google.tokengetter
def get_access_token():
    return session.get('access_token')

def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host=app.config['HOST'], port=port)

if __name__ == '__main__':
    main()
