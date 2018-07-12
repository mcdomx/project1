import os
import datetime
import requests, json


from flask import Flask, session, jsonify, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# darksky key
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


# FLASK ROUTES
# -------------------------------------------------------------

# site root
@app.route("/")
def index():
    # if no user is logged in, present user with login
    # if user is logged in already, present user with seach
    if session.get("user_session") is None:
        return render_template("index.html")
    else:
        return render_template("search.html", message="search for weather", user_session=session["user_session"])


# get login results
@app.route("/", methods=["POST"])
def login():
    # get data from login form
    user_id = str(request.form.get("user_id"))
    pwd = str(request.form.get("pwd"))

    # ensure both user_id and pw were provided
    if user_id=="" or pwd=="":
        #TODO display message
        return render_template("index.html", message="enter a user name and password", user_id=user_id, pwd=pwd)


    # check to see if supplied user_id exists
    if db.execute("SELECT * FROM tbl_users WHERE user_id=:id", {"id": user_id}).rowcount is 0:
        # no user exists
        return render_template("index.html", message="No user: " + user_id)
    else:
        # user exists - check passworsd
        user_credentials = db.execute("SELECT * FROM tbl_users WHERE user_id=:id", {"id": user_id}).fetchone()
        if pwd == user_credentials[2]:
            # password matches - login user
            if session.get("user_session") is None:
                session["user_session"] = []
            session["user_session"].append(user_credentials[0])
            session["user_session"].append(user_credentials[1])
            return render_template("search.html", message="login successful", user_session=session["user_session"])
        else: # if password is not correct
            return render_template("index.html", message="password incorrect", user_id=user_id, pwd=pwd)


# LOGOUT
@app.route("/logout")
def logout():
    # remove user_session from session variable
    session.pop("user_session", None)
    return render_template("index.html", message="Successfully logged out.")


# REGISTER
@app.route("/register")
def register():
    # display registration page
    return render_template("register.html")


# CREATE NEW USER
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
    else: # data is complete
        add_user(user_id, user_name, pwd)
        return render_template("registration_success.html", user_id=user_id, user_name=user_name)


# DISPLAY SEARCH RESULTS
@app.route("/search_result", methods=["POST"])
def search_result():
    search_value = str(request.form.get("location_input")).upper()

    if search_value == "":
        return render_template("search.html", message="enter a zip or town to search for")

    # Check for partial input of either a city or a zipcode
    search_results = db.execute("SELECT * FROM tbl_locations WHERE city LIKE :city OR zipcode LIKE :zip", {"city": "%" + search_value + "%" , "zip": "%" + search_value + "%"}).fetchall()
    result_count = len(search_results)

    if result_count==0:
        # no results found
        return render_template("search.html", message="no results found for: " + search_value, result_count=result_count, search_results=search_results)
    elif result_count==1:
        # If 1 result found, go straight to weather page
        return get_weather(search_results[0]["zipcode"])
    else:
        # multiple results found, show a list of results
        return render_template("search.html", message="found result for: " + search_value, result_count=result_count, search_results=search_results)


# DISPLAY LOCATION INFORMATION
@app.route("/weather/<string:zip>")
def get_weather(zip):
    # check to see that user is logged in - redirect to login page with message if not logged in
    if session.get("user_session") is None:
        return render_template("index.html", message="Must be logged in to see location information and weather.  Please log in.")

    # get location information
    loc_info = get_location_info(zip)

    # if no such zip code exists, post error and revert to search
    if loc_info == None:
        return render_template("search.html", message="no location results found for: " + zip)

    # Get weather data from Darksky for respectve zipcode
    weather = get_current_weather(zip)

    # if no such zip code exists, post error and revert to search
    if weather == None:
        return render_template("search.html", message="no weather results found for: " + zip)

    # Check to see if user has already posted a checkin comment.
    existing_checkin = checkin_exists(session["user_session"][0], zip)

    # Retireve checkin comments for the respective zipcode
    # loc_comments = db.execute("SELECT * FROM tbl_comments JOIN tbl_users ON tbl_comments.user_id=tbl_users.user_id WHERE zipcode=:zip ORDER BY tbl_comments.comment_id DESC", {"zip": zip}).fetchall()
    loc_comments = get_location_comments(zip)

    # Return location page with respective location and weather data
    return render_template("location.html", weather=weather, loc_info=loc_info, loc_comments=loc_comments, existing_checkin=existing_checkin)


# add a comment to a checking on a location page
@app.route("/weather/<string:zip>", methods=["POST"])
def add_comment(zip):

    # get comment from form on page
    new_comment = str(request.form.get("new_comment"))

    # insert comment into database
    db.execute("INSERT INTO tbl_comments (cmt_date, user_id, zipcode, comment) \
    VALUES (:cmt_date, :UID, :Zip, :Comment)",
        {"cmt_date":datetime.datetime.now(), "UID":session["user_session"][0], "Zip":zip, "Comment":new_comment})
    db.commit()

    # show updated location page with new comment
    return get_weather(zip)



# API SUPPORT
# Return JSON formatted result of location statistics for zipcode supplied as argument
# -------------------------------------------------------------
@app.route("/api/<string:zip>", methods=["GET"])
def zipweather_api(zip):
    # ensure zipcode exists - send error if not found
    if not check_zipcode(zip):
        return jsonify({"error": "Zipcode does not exist:" + zip}), 404

    # get location information from database
    loc_info = get_location_info(zip)

    # return the json request
    return jsonify({
            "place_name": loc_info.city,
            "state": loc_info.state,
            "latitude": loc_info.lat,
            "longitude": loc_info.lon,
            "zip": zip,
            "population": loc_info.population,
            "check_ins": count_checkins(zip)
        })



# SUPPORT FUNCTIONS
# -------------------------------------------------------------

# Check to see if zipcode exists in Database
# Return True if it exists. Return Flase if it does not.
def check_zipcode(zip):
        search_results = db.execute("SELECT * FROM tbl_locations WHERE zipcode=:zip", {"zip": zip }).fetchone()
        if search_results == None:
            return False
        else:
            return True

# Return the current weather in JSON format for supplied zip code argument
def get_current_weather(zip):
    loc_info = db.execute("SELECT * FROM tbl_locations WHERE zipcode=:zip", {"zip": zip}).fetchone()
    get_weather = "https://api.darksky.net/forecast/" + darksky_key + "/" + str(loc_info["lat"]) + "," + str(loc_info["lon"])
    weather = requests.get(get_weather).json()
    return weather['currently']

# Return row from table of locations of data for a zipcode supplied as an argument.
def get_location_info(zip):
    return db.execute("SELECT * FROM tbl_locations WHERE zipcode=:zip", {"zip": zip}).fetchone()

# Return the checkin comments for a supplied zipcode
def get_location_comments(zip):
    return db.execute("SELECT * FROM tbl_comments JOIN tbl_users ON tbl_comments.user_id=tbl_users.user_id WHERE zipcode=:zip ORDER BY tbl_comments.comment_id DESC", {"zip": zip}).fetchall()

# Check to see if user has already posted a checkin comment.
def checkin_exists(user_id, zip):
    return db.execute("SELECT * FROM tbl_comments WHERE user_id=:user_id AND zipcode=:zip", {"user_id" :session["user_session"][0], "zip": zip}).rowcount

# Count the number of checkins for a zipcode
def count_checkins(zip):
    search_results = db.execute("SELECT * FROM tbl_locations WHERE zipcode LIKE :zip", {"zip": "%" + zip + "%" }).fetchall()
    return len(search_results)

# add user into database
def add_user(user_id, user_name, pwd):
    db.execute("INSERT INTO tbl_users VALUES (:user_id, :user_name, :pwd)",
    {"user_id": user_id, "user_name": user_name, "pwd": pwd})
    db.commit()

# END SUPPORT FUNCTIONS ------------------------------------------



# FILTERS
# -------------------------------------------------------------

# jinja filter to convert epoch time to human readable format
@app.template_filter('format_time')
def convert_epoch(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time)

#END FILTERS --------------------------------------------------
