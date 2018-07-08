import os
import passlib
import datetime
import requests, json

from flask import Flask, session, jsonify, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
darksky_key = "ff036cf3d154f83b55a5261f6a293109"

# Check for environment variables
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("-- Environment variable DATABASE_URL is not set")

if not os.getenv("FLASK_APP"):
    raise RuntimeError("-- Environment variable FLASK_APP is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# site root
@app.route("/")
def index():
    # if no user is logged in, present user with login
    # if user is logged in already, present user with seach
    if session.get("user_session") is None:
        return render_template("index.html")
    else:
        return render_template("search.html", message="search for weather", user_session=session["user_session"])

# zipcode results
@app.route("/weather/<string:zip>")
def get_weather(zip):
    lat_lon = db.execute("SELECT lat,lon FROM tbl_locations WHERE zipcode=:zip", {"zip": zip}).fetchone()
    get_weather = "https://api.darksky.net/forecast/" + darksky_key + "/" + str(lat_lon[0]) + "," + str(lat_lon[1])
    weather = requests.get(get_weather).json()
    w = weather['currently']
    rv = "Zip: " + str(zip) + '\n'                  \
        + "Lat: " + str(lat_lon[0]) + '\n'              \
        + "Lon: " + str(lat_lon[1]) + '\n'              \
        + "Temp: " + str(w['temperature']) + '\n'       \
        + "Humidity: " + str(w['humidity']) + "\n"      \
        + "Wind Speed: " + str(w['windSpeed']) + "\n"   \
        + "Time: " + datetime.datetime.fromtimestamp(w['time']).strftime('%c')
    return rv

# use python hashlib or passlib to encrypt users Password
# sanitize password by escaping characters ' and "
@app.route("/", methods=["POST"])
def login():


    # get data from login form
    user_id = str(request.form.get("user_id"))
    pwd = str(request.form.get("pwd"))

    #ensure both user_id and pw were provided
    if user_id=="" or pwd=="":
        #TODO display message
        return render_template("index.html", message="enter a user name and password", user_id=user_id, pwd=pwd)


    if db.execute("SELECT * FROM tbl_users WHERE user_id=:id", {"id": user_id}).rowcount is not 0:
        # user exists - check passworsd
        user_credentials = db.execute("SELECT * FROM tbl_users WHERE user_id=:id", {"id": user_id}).fetchone()
        if pwd == user_credentials[2]:
            # password matches - login user
            if session.get("user_session") is None:
                session["user_session"] = []
            session["user_session"].append(user_credentials[0])
            session["user_session"].append(user_credentials[1])
            return render_template("search.html", message="login successful", user_session=session["user_session"])
        else:
            return render_template("index.html", message="password incorrect", user_id=user_id, pwd=pwd)
    else:
        return render_template("index.html", message="No user: " + user_id)


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user_session", None)
    return render_template("index.html", message="Successfully logged out.")



@app.route("/register")
def register():
    return render_template("register.html")
    # ensure all fields are filled out
    # ensure user_id is not "user_id"
    # ensure that user_id is not already taken
    #update the login form to show pwd confirmation and get a __name__


@app.route("/create_user", methods=["POST"])
def create_user():
    # get data from login form
    user_id = str(request.form.get("user_id"))
    user_name = str(request.form.get("user_name"))
    pwd = str(request.form.get("pwd"))
    pwd_conf = str(request.form.get("pwd_conf"))

    #if any field is not filled in, re-display form with message
    if user_id=="" or user_name=="" or pwd=="" or pwd_conf=="":
        message = "Fill in all fields"
        return render_template("register.html", message=message)
    elif pwd != pwd_conf:
        #make sure that passwords match
        message = "Password does not match."
        return render_template("register.html", message=message)
    else:
        add_user(user_id, user_name, pwd)
        return render_template("registration_success.html", user_id=user_id, user_name=user_name)

# add user into database
def add_user(user_id, user_name, pwd):
    db.execute("INSERT INTO tbl_users VALUES (:user_id, :user_name, :pwd)",
    {"user_id": user_id, "user_name": user_name, "pwd": pwd})
    db.commit()


@app.route("/search_result", methods=["POST"])
def search_result():
    search_value = str(request.form.get("location_input")).upper()

    if search_value == "":
        return render_template("search.html", message="enter a zip or town to search for")

    # result_rows = db.execute("SELECT * FROM tbl_locations WHERE zipcode=:zip", {"zip": search_value}).rowcount

    # result_count = db.execute("SELECT * FROM tbl_locations WHERE zipcode LIKE :zip", {"zip": "%" + search_value + "%" }).rowcount
    search_results = db.execute("SELECT * FROM tbl_locations WHERE zipcode LIKE :zip", {"zip": "%" + search_value + "%" }).fetchall()
    result_count = len(search_results)

    # if no matches in the zip code field are found, check the city name
    if result_count==0:
        # result_count = db.execute("SELECT * FROM tbl_locations WHERE city LIKE :city", {"city": "%" + search_value + "%" }).rowcount
        search_results = db.execute("SELECT * FROM tbl_locations WHERE city LIKE :city", {"city": "%" + search_value + "%" }).fetchall()
        result_count = len(search_results)

    if result_count==0:
        # no results found
        return render_template("search.html", message="no results found for: " + search_value, result_count=result_count, search_results=search_results)
    elif result_count==1:
        # go straigh to weather page
        return render_template("search.html", message="found result for: " + search_value, result_count=result_count, search_results=search_results)
    else:
        # multiple results found - show a list of results
        return render_template("search.html", message="found result for: " + search_value, result_count=result_count, search_results=search_results)


    # try:
    #     flight_id = int(request.form.get("flight_id"))
    # except ValueError:
    #     return render_template("error.html", message="Invalid flight number.")
