# Project 1 - ZipWeather
Web Programming with Python and JavaScript

##Overview
In this project, I tried to keep the navigation and user interface as simple as possible.  My general approach was to disallow the user from doing anything that was not permitted to avoid the need to trap errors and present the user with a frustrating response.  For example, since users can only make one Check-In per location, if the user has a documented check-in, the user is not presented with an input box for a comment.

A single application.py file is used for the Python support code.  An SCSS file is used for the CSS stylesheet.  Bootstrap is used for various formatting items.

jinja2 is used in conjunction with the Python code to present templates as web pages.  A single layout page was used for all pages of the site to keep a consistent look and feel.

Test user comments were posted to zipcode 02138 for demonstration and testing purposes.  

A jinja2 filter was created to display the epoch time in user readable format.

###Running the application
The application can be run by starting flask from the root project directory ("flask run") and then navigating to the link that flask returns after issuing the run command.

If the application is not run from my environment, the following commands are necessary to setup necessary environment variables:
export DATABASE_URL=postgres://vgltksvpsmnavf:5824aaa0eb811eb3aafefbdce73bd490e76ef577231e1b3632c23d64503f7539@ec2-107-20-193-202.compute-1.amazonaws.com:5432/d6avrg1hsn8aje
export FLASK_APP=application.py
export FLASK_DEBUG=1

###Registration
The registration process is initiated with a link from the index page.  Once the user enters appropriate registration information, a confirmation message is presented to the user and the user is forced to login with their new credentials.  No "forgot password" process was implemented.  Successful registration updates the user table in the database with the new user and respective user data.

For this project, the registration validation is limited to completing all the field (email, Name, password, password confirmation) and that the password and the password confirmation match.  Bootstrap handles the email format validation and obscures the password fields.

###Login/Logout
Keeping security in mind, the user id is not presented except when confirming a registration.  No other security measures were implemented.

Once a user is logged in, the user's name is presented in the top right of the site along with a link to logout.

Session variables are used to keep track of the logged in user's credentials and respective information.  The user will remain logged until the user explicitly logs out.  No auto-logout or timeout-logout is implemented.

###Search
Searching for weather is only possible when a registered user is logged in.  Once logged in, the user is presented with a search page where a zip code or city can be entered.  A partial zip code or city name will return all the results that match the partial result.  If only one result is found, the user is directed directly to the weather page for the location; otherwise, the user is presented with a list of possible matches and must select from an item in the list.

###Location page
Once on the location page, the user is presented with another search box to initiate another search as well as location data and the current weather.  The bottom section of the page includes checkins posted by registered users.  Since a user can only post a single checkin per location (zip code), if the user has already posted a checkin comment, then there is no possibility to enter another comment.

###API
As required, a simple API was implemented that returns the location information for a zipcode in JSON format.

###Helper Functions
In order to keep the main functions easy to follow, 5 helper functions are used to handle some basic support tasks.  These are listed at the bottom of the application.py file.  One of them is the jinja2 custom filter to display epoch time in readable format.



##Requirements

###Registration:
- [X] Users should be able to register for your website, providing (at minimum) a username and password.

###Login:
- [X] Users, once registered, should be able to log in to your website with their username and password.

###Logout:
- [X] Logged in users should be able to log out of the site.

###Import:
- [X] Provided for you in this project is a file called zips.csv, which is a file in CSV format of all ZIP codes in the United States that have a population of 15,000 or more as well as some other information such as location names and short codes, latitude and longitude, and population. In a Python file called import.py separate from your web application, write a program that will take the information in this CSV and import it into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python import.py to import the books into your database, and submit this program with the rest of your project code.

###Search:
- [X] Once a user has logged in, they should be taken to a page where they can search for a location. Users should be able to type a ZIP code or the name of a city or town. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches at all. If the user typed in only partial information, your search page should find matches for those as well!

###Location Page:
- [X] When users click on a location from the results of the search page, they should be taken to a page for that location, with details about the location coming from your database: the name of the location, its ZIP code, its latitude and longitude, its population, and the number of check-ins and the written comments that users have left for the location on your website.

###Check-In Submission:
- [X] On the location page, users should be able to submit a “check-in”, consisting of a button that allows them to log a visit, as well as a text component where the user can provide comments about the location. Users should not be able to submit more than one check-in for the same location or edit a comment they have previously left. Users should only be able to submit a check-in if they are logged in.

###Dark Sky Weather Data:
- [X] On your location page, you should also display information about the current weather, displaying minimally the time of the weather report, the textual weather summary (e.g. “Clear”), temperature, dew point, and humidity (as a percentage). You can display more information if you wish.

###API Access:
- [X] If users make a GET request to your website’s /api/<zip> route, where <zip> is a ZIP code, your website should return a JSON response containing (at a minimum) the name of the location, its state, latitude, longitude, ZIP code, population, and the number of user check-ins to that location. The resulting JSON should follow the format; the order of the keys is not important, so long as they are all present:
{
    "place_name": "Cambridge",
    "state": "MA",
    "latitude": 42.37,
    "longitude": -71.11,
    "zip": "02138",
    "population": 36314,
    "check_ins": 1
}
If the requested ZIP code isn’t in your database, your website should return a 404 error.

###README.md
In README.md, include a short write-up describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!
Beyond these requirements, the design, look, and feel of the website are up to you! You’re also welcome to add additional features to your website, so long as you meet the requirements laid out in the above specification!
