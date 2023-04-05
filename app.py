# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify, make_response
# from  flask_mysqldb import MySQL
import pymysql
from hashlib import pbkdf2_hmac
from flask_cors import CORS
# imports for PyJWT authentication
import jwt
from werkzeug.utils import secure_filename
# import MySQLdb.cursors
from functools import wraps
import re
import os


# set up flask application
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG']
app.config['UPLOAD_PATH'] = 'File'
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
JWT_SECRET_KEY="SomeRandomSecretKey"
app.secret_key = 'happykey'
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'test'
# To connect MySQL database
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password="root",
    db='449_db',
)

cur = conn.cursor()

#error handle
#done

@app.route('/')
# error hendling
@app.errorhandler(400)
def bed_request(e):
    return render_template('400.html'), 400


@app.errorhandler(401)
def unauthorized(e):
    return make_response("error 401", 401)
    return render_template('401.html'), 401


@app.errorhandler(403)
def forbidden(e):
    return make_response("error 403", 403)
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return make_response("error 404", 404)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_Server_error(e):
    return make_response("error 500", 500)
    return render_template('500.html'), 500


# Authentication
# need to change to JWT
def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["username"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False
        
def generate_salt():
    salt = os.urandom(16)
    return salt.hex()

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

def db_write(query, params):
    cur.execute(query, params)
    conn.commit()

    return True

def db_read(query, params=None):
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    entries = cur.fetchall()
    content = []
    for entry in entries:
        content.append(entry)

    return content


def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    print(str(encoded_content))
    token = str(encoded_content).split(".")[1]
    return token

def validate_user(username, password):
    current_user = db_read("""SELECT * FROM user WHERE username = %s""", (username,))

    print(current_user)
    if len(current_user) == 1:
        saved_password_hash = current_user[0][3]
        saved_password_salt = current_user[0][2]
        password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user[0][0]
            jwt_token = generate_jwt_token({"id": user_id})
            return jwt_token
        else:
            return False

    else:
        return False
    
@app.route('/login', methods =['POST'])
def login():
    user_name = request.json["username"]
    user_password = request.json["password"]
    user_token = validate_user(user_name, user_password)
    if user_token:
        return jsonify({"jwt_token": user_token})
    else:
        abort(401)


@app.route('/signup', methods =['POST'])
def signup():
    print(request)
    user_name = request.json["username"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]

    if user_password == user_confirm_password and validate_user_input(
        "authentication", username=user_name, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        if db_write(
            """INSERT INTO user (username, password_salt, password_hash) VALUES (%s, %s, %s)""",
            (user_name, password_salt, password_hash),
        ):
            # Registration Successful
            return make_response("success sinup")
        else:
            # Registration Failed
            return make_response("Registration Failed")
    else:
        # Registration Failed
        abort(400)

# upload file api
# done
@app.route("/uploadfile", methods=['post'])
def uploadfile():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return make_response("file upload success")
    # return redirect(url_for('index'))


# public route
# done
# the page do not need Authentication and every can acess tis api
@app.route("/publicroute")
def publicroute():
    return make_response("every one can use this")


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
