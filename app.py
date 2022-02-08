from flask import Flask, render_template, redirect, request, session
import mysql.connector, re, os
from dotenv import load_dotenv

app = Flask(__name__)


load_dotenv()
app.config["SECRET_KEY"] = os.getenv('SESSION_SECRET')

@app.route("/")
def index():

    return redirect("/signup")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
        cursor = cnx.cursor(buffered=True)  
        if not request.form.get("fname"):
            return ("No email")
        if not request.form.get("lname"):
            return("NO PASSWORD")

        email_form = request.form.get("fname")
        password_form = request.form.get("lname")

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if (re.fullmatch(regex, email_form)):
            print("Valid Email")
        else:
            return("Invalid Email")

        # email_exist = ("SELECT user_email FROM users_list")
        # email_exist = cursor.execute(email_exist)
        # myresult = cursor.fetchall()
        # print("emails", myresult)


        email_exist = ("SELECT EXISTS (SELECT user_email FROM users_list WHERE user_email = '{}')".format(email_form))
        cursor.execute(email_exist)
        email_exist = cursor.fetchall()

        if email_exist[0][0] == True:
            return("THIS E-MAIL ADDRESS IS ALREADY REGISTERED")
        

        if len(password_form) < 8:
            print("Less than 8")
        uppercase = 0
        lowercase = 0
        numeric = 0
        for i in password_form:
            if i.isupper():
                uppercase += 1
                print(i, "upper")
            elif i.islower():
                lowercase += 1
                print(i, "low")
            elif i.isnumeric():
                numeric += 1
                print(i, "number")
        if uppercase < 2:
            return("Password should contain at least 2 letters in uppercase")
        elif lowercase < 3:
            return("Password should contain at least 3 letters in lowercase")
        elif numeric < 3:
            return("Password should contain at least 3 numbers")


        signup_push = ("INSERT INTO users_list (user_email, user_password)" "VALUES (%s, %s)")
        user_data = (email_form, password_form)
        cursor.execute(signup_push, user_data)
        cnx.commit()

    return render_template("signup.html", name="BOB")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cnx = mysql.connector.connect(user='root', password='password123', host='127.0.0.1', database='users')
        cursor = cnx.cursor(buffered=True)  
        if not request.form.get("fname"):
            return ("No email")
        if not request.form.get("lname"):
            return("NO PASSWORD")

        email_form = request.form.get("fname")
        password_form = request.form.get("lname")

        password_match = ("SELECT user_password, user_id FROM users_list WHERE user_email = '{}'".format(email_form))
        cursor.execute(password_match)
        password_match = cursor.fetchall()

        if password_form != password_match[0][0]:
            return("WRONG PASSWORD")

        session["user_id"] = password_match[0][1]
        print(session)

    return render_template("login.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
   
    return render_template("forgot_password.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return redirect("/signup")