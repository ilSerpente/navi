from cgitb import reset
from concurrent.futures import thread
import email
from email.policy import default
import json
from sqlite3 import Timestamp
import threading
from threading import Thread
import time
from types import new_class
from unicodedata import name
from flask import Flask, render_template, redirect, request, session, render_template_string, send_from_directory
import mysql.connector
import re
import os
import string
import random
from dotenv import load_dotenv
from flask_mail import Mail, Message
from lattolat import all_data_reader
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from appp import data_collector


# app = Flask(__name__)
app = Flask(__name__, static_folder='../navi_interface/build')
app.debug = True
CORS(app)

uri = os.getenv("URL")
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Users_data']
collection = db['Users']

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")
mail = Mail(app)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv('SESSION_SECRET')


def printer():
    global last_update_time
    global trucks
    last_update_time = 0
    trucks = {}
    while True:
        _, trucks_obj_dict, timestamp = all_data_reader(trucks)
        print("Printer")
        trucks = trucks_obj_dict
        last_update_time = timestamp
        time.sleep(60)


t1 = Thread(target=printer)
t1.start()
print(t1.is_alive())


def email_exist_fuction(email_exist):
    cnx = mysql.connector.connect(
        user='root', password='password123', host='127.0.0.1', database='users')
    cursor = cnx.cursor(buffered=True)
    email_exist = ("SELECT EXISTS (SELECT user_email FROM users_list WHERE user_email = '{}')".format(
        request.form.get("fname")))
    cursor.execute(email_exist)
    email_exist = cursor.fetchall()
    return(email_exist)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        print(path)
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/', defaults={'name': ""})
@app.route('/<path:name>')
def route_css(name):
    print(name)
    if name != "":
        return send_from_directory(app.static_folder, name)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# @app.route('/abc/<int:name>')
# def abc(name):
#     print(name)
#     return jsonify("wadsdawd +  {}".format(name))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.json
        email = data.get('email')
        password = data.get('password')
        email_exist = collection.find_one({"user_email": email})
        if email_exist == None:
            collection.insert_one({"user_email": email, "user_password": password})
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return 409


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if email and password != None:
            access_token = create_access_token(identity=email)
            response_data = {'access_token': access_token}
            return jsonify(response_data), 200
        else:
            response_data = {'message': 'Invalid credentials'}
            return jsonify(response_data), 401


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":
        if not request.form.get("fname"):
            return ("NO EMAIL ADDRESS ADDED")

        cnx = mysql.connector.connect(
            user='root', password='password123', host='127.0.0.1', database='users')
        cursor = cnx.cursor(buffered=True)

        email_form = request.form.get("fname")

        email_exist = email_exist_fuction(request.form.get("fname"))

        if email_exist[0][0] == 0:
            return("WRONG EMAIL ADDRES")

        reset_password = []

        for i in range(8):
            if i <= 1:
                reset_password += random.sample(string.ascii_uppercase, 1)
            if i > 1 and i <= 4:
                reset_password += random.sample(string.digits, 1)
            if i > 4 and i <= 8:
                reset_password += random.sample(string.ascii_lowercase, 1)

        reset_password = "".join(reset_password)

        change_password = ("UPDATE users_list SET user_password = {} WHERE user_email = {};".format(
            reset_password, email_form))

        msg = Message()
        msg.subject = "Password reset"
        msg.recipients = [email_form]
        msg.sender = os.getenv("EMAIL")
        msg.body = 'Your new password: {}'.format(reset_password)
        mail.send(msg)
        return redirect("/login")

    return render_template("/forgot_password.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("user_id"):
        return redirect("/login")
    (fig, number_plates) = get_map()
    div = fig.to_html(full_html=False)

    return render_template("dashboard.html", div_placeholder=div, number_plates=number_plates)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/number/<int:timestamp>")
def number(timestamp):

    trucks_dict = {"list": {}, "timestamp": last_update_time}

    for truck in trucks.values():
        if truck.last_update_time > timestamp:
            trucks_dict["list"][truck.truck_id] = truck.as_dict()

    trucks_json = json.dumps(trucks_dict, indent=4)
    return trucks_json
