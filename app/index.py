from flask import render_template, session, redirect, url_for, request, jsonify
from app import IssueTracker
from app.tools.hashTools import Hash
from app.tools.faceUnlock import FaceUnlock
from app.tools.dbTools import DataBaseManager

IssueTracker.secret_key = "SecretUserUI##187782####"


@IssueTracker.route("/", methods=['GET'])
def index():
    if 'authorized' in session and session['authorized'] is True:
        return redirect(url_for("render_main_issue_list"))

    return render_template("index.html")


def create_face_session_for(face, username):
    print(username)
    if face and (username is not ""):
        session['user'] = username
        session['authorized'] = True

        return True
    return False


def create_session_for(username, password):
    pwd_manager = Hash()
    if pwd_manager.check_password(username, password):
        session['user'] = username
        session['authorized'] = True

        return True
    return False


@IssueTracker.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        if create_session_for(username, password):
            return redirect(url_for('render_main_issue_list'))

    return render_template("index.html", error=True, username=username)


@IssueTracker.route('/face_unlock', methods=['POST', 'GET'])
def face_unlock():
    username = request.form.get('var2')
    picture = request.form.get('var1')

    if username is not "":
        user = DataBaseManager.check_existing_user_name(username)
        if user:
            FaceUnlock.upload_s3(picture, username)
            key1 = username + '_master.jpg'
            key2 = username + '.jpg'
            response = FaceUnlock.face_match(key1, key2)
            if create_face_session_for(response, username):
                return redirect(url_for('render_main_issue_list'))

    return render_template("index.html", error=True, username=username)
