from cgitb import reset
import email
from email.policy import default
import json
from flask import Flask, render_template, redirect, request, session, render_template_string, send_from_directory
import mysql.connector, re, os, string, random
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

app = Flask(__name__, static_folder='../navi_interface/build')
app.debug=True
CORS(app)

uri = "mongodb+srv://dbarannik97:qwerty123@cluster0.4qj9xmn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Users_data']
collection = db['Users']

app.config["JWT_SECRET_KEY"] = "MikeWasowski"
jwt = JWTManager(app)

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")
mail = Mail(app)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv('SESSION_SECRET')

def email_exist_fuction(email_exist):
    cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
    cursor = cnx.cursor(buffered=True)  
    email_exist = ("SELECT EXISTS (SELECT user_email FROM users_list WHERE user_email = '{}')".format(request.form.get("fname")))
    cursor.execute(email_exist)
    email_exist = cursor.fetchall()
    return(email_exist)

# @app.route("/")
# def index():
#     if not session.get("user_id"):
#         return redirect("/signup")
#     return redirect('/dashboard')
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
        email_exist = collection.find_one({"user_email":email})
        if email_exist == None:
            collection.insert_one({"user_email":email, "user_password": password})
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return 409
        

# def signup():
#     if request.method == "POST":
#         cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
#         cursor = cnx.cursor(buffered=True)  
#         if not request.form.get("fname"):
#             return ("No email")
#         if not request.form.get("lname"):
#             return("NO PASSWORD")

#         email_form = request.form.get("fname")
#         password_form = request.form.get("lname")

#         regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#         if (re.fullmatch(regex, email_form)):
#             print("Valid Email")
#         else:
#             return("Invalid Email")

#         email_exist = email_exist_fuction(request.form.get("fname"))

#         if email_exist[0][0] == True:
#             return("THIS E-MAIL ADDRESS IS ALREADY REGISTERED")
        

#         if len(password_form) < 8:
#             print("Less than 8")
#         uppercase = 0
#         lowercase = 0
#         numeric = 0
#         for i in password_form:
#             if i.isupper():
#                 uppercase += 1
#                 print(i, "upper")
#             elif i.islower():
#                 lowercase += 1
#                 print(i, "low")
#             elif i.isnumeric():
#                 numeric += 1
#                 print(i, "number")
#         if uppercase < 2:
#             return("Password should contain at least 2 letters in uppercase")
#         elif lowercase < 3:
#             return("Password should contain at least 3 letters in lowercase")
#         elif numeric < 3:
#             return("Password should contain at least 3 numbers")


#         signup_push = ("INSERT INTO users_list (user_email, user_password)" "VALUES (%s, %s)")
#         user_data = (email_form, password_form)
#         cursor.execute(signup_push, user_data)
#         cnx.commit()
#         return redirect("/dashboard")
#     return render_template("signup.html")

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
            
    # if request.method == "POST":
    #     cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
    #     cursor = cnx.cursor(buffered=True)  
    #     if not request.form.get("fname"):
    #         return ("No email")
    #     if not request.form.get("lname"):
    #         return("NO PASSWORD")

    #     email_form = request.form.get("fname")
    #     password_form = request.form.get("lname")

    #     email_exist = email_exist_fuction(request.form.get("fname"))

    #     if email_exist[0][0] == False:
    #         return("THIS E-MAIL ADDRESS IS NOT REGISTERED")

    #     password_match = ("SELECT user_password, user_id FROM users_list WHERE user_email = '{}'".format(email_form))
    #     cursor.execute(password_match)
    #     password_match = cursor.fetchall()

    #     if password_form != password_match[0][0]:
    #         return("WRONG PASSWORD")

    #     session["user_id"] = password_match[0][1]
    #     return redirect("/dashboard")
    # return render_template("/login.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    
    if request.method == "POST":
        if not request.form.get("fname"):
            return ("NO EMAIL ADDRESS ADDED")

        cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
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
 
        change_password = ("UPDATE users_list SET user_password = {} WHERE user_email = {};".format(reset_password, email_form))

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



@app.route("/number")
def number():
    trucks = all_data_reader()[1]
    trucks_dict = {"list": []}

    for truck in trucks:
        trucks_dict["list"].append(truck.as_dict())

    trucks_json = json.dumps(trucks_dict, indent=4)
    return trucks_json




