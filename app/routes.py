from app import app, db
from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response
from models import User
from config import CLIENT_ID
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from oauth2client import crypt

@app.route("/index")
def index():
    return "Hello"

@app.route('/auth/google', methods = ['POST'])
def login():
    try:
        auth_token = request.values.get('oauth_token')
        debug(auth_token)
    except AttributeError:
        response = make_response(json.dumps("No token provided"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    err = ''
    idinfo = None
    try:
        idinfo = client.verify_id_token(auth_token, CLIENT_ID)
        debug(idinfo)
    
    except crypt.AppIdentityError:
        # Invalid token
        err =  err if err else "Failed to verify token"
        debug("error was: " + err)
        response = make_response(json.dumps("Invalid token: {}".format(err)), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        

    debug("Step 2 Complete! Access Token : %s " % auth_token)


    ##TODO.
    if not idinfo["email_verified"]:
        pass

    #see if user exists, if it doesn't make a new one
    user = User.query.filter_by(email=idinfo['email']).first()
    if not user:
        user = User(
            username = idinfo['name'],  
            email = idinfo['email'])
        db.session.add(user)
        db.session.commit()


    return jsonify({'auth_token': "abc"})

@app.route('/user', methods = ['POST'])
def getUser():
    try:
        email = request.values.get('email')
        debug(email)
    except AttributeError:
        response = make_response(json.dumps("No token provided"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    user = User.query.filter_by(email=email).first()
    return jsonify({"username":user.username}) 


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/abc", methods = ["GET"])
def abc():
	return "abc"

def debug(s):
    print(s)

