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
    weather = requests.get("https://api.darksky.net/forecast/ff036cf3d154f83b55a5261f6a293109/42.37,-71.11").json()
    w = weather['currently']
    rv = "Temp: " + str(w['temperature']) + '\n'    \
        + "Humidity: " + str(w['humidity']) + "\n"  \
        + "Time: " + datetime.datetime.fromtimestamp(w['time']).strftime('%c')
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
def book():

    # get data from login form
    user_id = str(request.form.get("user_id"))
    pw = str(request.form.get("pw"))

    # ensure user_id is not "user_id"
    # ensure that user_id is not already taken
    # ensure all fields are filled out
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
