# This module will load data from zips.csv into the application's database
# source file format:
#   Zipcode,City,State,Lat,Long,Population (header line)
#

# database structures
# weather locations
CREATE TABLE locations {
    zipcode VARCHAR PRIMARY KEY,
    city VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    population INTEGER NOT NULL,
}

# user
CREATE TABLE users {
    user_id VARCAHR PRIMARY KEY,
    password VARCHAR
}

# comments
CREATE TABLE comments {
    comment_id SERIAL PRIMARY KEY,
    user_id VARCAHR,
    zipcode INTEGER,
    comment VARCHAR
}

# inserting data into table
INSERT INTO locations
    (zipcode, city, state, lat, lon, population)
    VALUES( , ' ', ' ', , , );

INSERT INTO comments
    (user_id, zipcode, comment)
    VALUES('mcdomx', '02138', 'super nice place');

# selecting data from Database
SELECT * FROM locations; #selects all items from locations
SELECT lot, lon FROM locations WHERE city = "Boston" OR zip = "02138";
SELECT AVG(population) FROM locations WHERE lat > 45;
SELECT COUNT(*) FROM locations WHERE city = "Springfield";
SELECT * FROM locations WHERE city LIKE '%Spring%;' # '%' is wildcard

# updating table data
UPDATE comments
    SET comment = 'really nice place'
    WHERE comment_id = 1;
