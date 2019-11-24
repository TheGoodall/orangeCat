from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

import organisor

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

import mysql.connector

cnx = mysql.connector.connect(
    user='root', password='KtvGEJmNHsvo7mJl',
    host='35.242.131.39', database='orangeCat'
)
cursor = cnx.cursor()

app = Flask(__name__)
app.secret_key = 'Xz\x04\xd29\xec\xc3_\x1c\xeb|\xc0zoO\x1a\xff\x9e\xf3\xf3^\x91U>'

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='TnIIJCX5qPCXbsVXIwfEWedNmw5sDqtx',
    client_secret='XDk-9CR-2q3AZtePZ1IelyY2QdfojHGsCyGUcowgFZ77ahO5SH58OabXnSbySPIl',
    api_base_url='https://dev-orange-cat.eu.auth0.com',
    access_token_url='https://dev-orange-cat.eu.auth0.com/oauth/token',
    authorize_url='https://dev-orange-cat.eu.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email'
    },
)

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token(redirect_uri='http://localhost:3000/callback')
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['user_id'] = userinfo['sub']
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:3000/callback')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('index', _external=True), 'client_id': 'TnIIJCX5qPCXbsVXIwfEWedNmw5sDqtx'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated


@app.route('/')
def index():
    if 'profile' in session:
        return redirect(url_for("dashboard"))
    return render_template('index.html', loggedin=session)

#Frontend endpoints
@app.route('/dashboard')
@requires_auth
def dashboard():
    cursor.execute("select * from tutee where tutee_id=%s", (session['profile']['user_id'],))
    result = cursor.fetchall()
    account_exists = False
    tutortype = ""
    for r in result:
        print(r)
        account_exists = True
        tutortype = "tutee"
    cursor.execute("select * from tutor where tutor_id=%s", (session['profile']['user_id'],))
    result = cursor.fetchall()
    for r in result:
        accound_exists = True
        tutortype = "tutor"


    return render_template('dashboard.html', loggedin=session, account_exists=account_exists, tutortype=tutortype)

@app.route('/dashboard/tutor')
@requires_auth
def tutor():
    cursor.execute("select * from subject")
    result = cursor.fetchall()
    data = [i for i in result]
    return render_template('tutor.html', loggedin=session, data=data)

@app.route('/dashboard/tutee')
@requires_auth
def tutee():
    cursor.execute("select * from subject")
    subjects = [s for s in cursor.fetchall()]
    cursor.execute("select * from times")
    times = [t for t in cursor.fetchall()]
    return render_template('tutee.html', loggedin=session, subjects=subjects, times=times)

@app.route('/dashboard/tutee-signup', methods=["POST"])
def tutee_signup():
    if request.form['fname'] and request.form['sname'] and request.form['first_subject'] and request.form['second_subject']:
        fname = request.form['fname']
        sname = request.form['sname']
        first_subject = request.form['first_subject']
        second_subject = request.form['second_subject']
        cursor.execute("insert into tutee values (%s, %s, %s, %s, %s);",
            (session['user_id'], first_subject, second_subject, fname, sname))
        for time_id in request.form.getlist('time'):
            print(session['user_id'], time_id)
            cursor.execute("insert into tutee_time values (%s, %s)",
                (session['user_id'], time_id))
        cnx.commit()
        return redirect(url_for("dashboard"))
    else:
        return 400

@app.route('/dashboard/tutor-signup', methods=["POST"])
def tutor_signup():
    return request.args.get("name")


#API endpoints




app.run(host='0.0.0.0', port=3000, debug=True)

cursor.close()
cnx.close()
