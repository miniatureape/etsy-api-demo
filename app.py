from flask import Flask
from flask import flash
from flask import url_for
from flask import redirect
from flask import jsonify
from flask import request
from flask import session
from flask import render_template
from flask.ext.oauth import OAuth

app = Flask(__name__)

"""
Put CONSUMER_KEY and CONSUMER_SECRET from etsy.com api sign up proccess in a 
file called settings.py:

CONSUMER_KEY = '<your key>'
CONSUMER_SECRET = '<your secret>'
"""

app.config.from_object('settings')

"Change this to your own secret"
app.secret_key = 'A0Zasklajsd3975428998j/3yX LWX/,?RT'

"Use sandbox.openapi.etsy.com/v2/ for the sandbox environment."
API_SERVER = 'http://openapi.etsy.com/v2/'
ETSY_SERVER = 'http://etsy.com/'

oauth = OAuth()

etsy = oauth.remote_app('etsy', 
    base_url=API_SERVER,
    request_token_url='%soauth/request_token' % API_SERVER,
    access_token_url='%soauth/access_token' % API_SERVER,
    authorize_url='%soauth/signin' % ETSY_SERVER,
    consumer_key=app.config['CONSUMER_KEY'],
    consumer_secret=app.config['CONSUMER_SECRET'],
    request_token_params={
        'scope': 'email_r listings_r cart_rw',
        'oauth_consumer_key': app.config['CONSUMER_KEY']
    }
)

@etsy.tokengetter
def get_etsy_token():
    return session.get('etsy_token')

@app.route("/")
def index():
    return render_template('index.html', login_url=url_for('login'))

@app.route("/login")
def login():
    next_url = request.args.get('next') or request.referrer or None
    callback_url = url_for('oauth_authorized', next=next_url, _external=True)
    return etsy.authorize(callback=callback_url)

@app.route("/logout")
def logout():
    session.pop('etsy_token')
    return redirect(url_for('index'))

@app.route("/authorized")
@etsy.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')

    if resp is None:
        flash(u'You need to give us access!')
        return redirect(url_for('index'))
    
    session['etsy_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret'],
    )

    return redirect(url_for('show_cart_contents'))

@app.route("/user/cart")
def show_cart_contents():
    "Grab some cart and user information"
    user_resp = etsy.get('users/__SELF__/') # __SELF__ is replaced with oauth'd userid by API
    cart_resp = etsy.get('users/__SELF__/carts/')
    return render_template('carts.html', carts=cart_resp.data, user=user_resp.data, logout_url=url_for('logout'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")

