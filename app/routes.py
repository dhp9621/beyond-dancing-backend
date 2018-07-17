from app import app, db
from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response
from app.models import User, Video
from app.config import CLIENT_ID, VIDEO_BUCKET, THUMBNAIL_BUCKET, BASE_S3_URL
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from oauth2client import crypt
import boto3
import os
import hashlib
import json
@app.route("/")
@app.route("/index")
def index():
    return make_response("Ok", 200)

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

@app.route('/uploadVideo', methods = ['POST'])
def uploadVideo():
    try:
        video_file = request.files['video']
        thumbnail_file = request.files['thumbnail']
        email = request.values.get('email')
        title = request.values.get('title')
    except AttributeError:
        response = make_response(json.dumps("token not provided"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    file_key = hashlib.sha224(email+title).hexdigest()
    s3 = boto3.client('s3')

    try:
        s3.upload_fileobj(video_file, VIDEO_BUCKET, file_key + '.mp4', ExtraArgs={'ACL':'public-read'})
        s3.upload_fileobj(thumbnail_file, THUMBNAIL_BUCKET, file_key + '.png', ExtraArgs={'ACL':'public-read'})
    except Exception as e: 
        response = make_response(json.dumps("Cant upload the file to S3"), 501)
        response.headers['Content-Type'] = 'application/json'
        return response

    video_url = os.path.join(BASE_S3_URL, VIDEO_BUCKET, file_key + '.mp4')
    thumbnail_url = os.path.join(BASE_S3_URL, THUMBNAIL_BUCKET, file_key + '.png')
    video = Video(user_email=email, title=title, video_url=video_url, thumbnail_url=thumbnail_url, likes=0, dislikes=0)
    db.session.add(video)
    db.session.commit()
    return make_response(json.dumps("Video uploaded"), 200)


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



def debug(s):
    print(s)

