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
    return render_template("index.html")

# zipcode results
@app.route("/<string:zipcode>")
def zip(zipcode):
    lat_lon = db.execute("SELECT lat,lon FROM tbl_locations WHERE zipcode=zipcode").fetchone()
    get_weather = "https://api.darksky.net/forecast/" + darksky_key + "/" + str(lat_lon[0]) + "," + str(lat_lon[1])
    weather = requests.get(get_weather).json()
    w = weather['currently']
    rv = "Zip: " + str(zipcode) + '\n'                  \
        + "Lat: " + str(lat_lon[0]) + '\n'              \
        + "Lon: " + str(lat_lon[1]) + '\n'              \
        + "Temp: " + str(w['temperature']) + '\n'       \
        + "Humidity: " + str(w['humidity']) + "\n"      \
        + "Wind Speed: " + str(w['windSpeed']) + "\n"   \
        + "Time: " + datetime.datetime.fromtimestamp(w['time']).strftime('%c')
    return rv

# use python hashlib or passlib to encrypt users Password
# saitize password by escaping characters ' and "
@app.route("/login", methods=["POST"])
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
            return render_template("index.html", message="login successful", user_name=user_credentials[1], user_id=user_id, pwd=pwd)
        else:
            return render_template("index.html", message="password incorrect", user_id=user_id, pwd=pwd)
    else:
        return render_template("login.html", message="no such user", user_id=user_id)



@app.route("/register", methods=["POST"])
def register(user_id, pwd):
    #ensure both user_id and pw were provided
    if user_id==None or pwd==None:
        #display message
        return render_template("login.html", user_id=user_id, pwd=pwd)
    # ensure all fields are filled out
    # ensure user_id is not "user_id"
    # ensure that user_id is not already taken
    #update the login form to show pwd confirmation and get a __name__


@app.route("/create_user", methods=["POST"])
def create_user(user_id, name, pwd, pwd_conf):
    #make sure that passwords match
    if pwd is not pwd_conf:
        #TODO display message
        return render_template("register.html", user_id=user_id, pwd=pwd)

    #add the user info to tbl_users



    # try:
    #     flight_id = int(request.form.get("flight_id"))
    # except ValueError:
    #     return render_template("error.html", message="Invalid flight number.")
