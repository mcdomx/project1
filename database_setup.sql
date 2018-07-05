# source file format:
#   Zipcode,City,State,Lat,Long,Population (header line)
#

# -----------------------------------------------------------
# database structures
# -----------------------------------------------------------
# weather locations
CREATE TABLE locations {
    zipcode VARCHAR PRIMARY KEY,
    city VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    population INTEGER NOT NULL,
}

# user table
CREATE TABLE users {
    user_id VARCAHR PRIMARY KEY,
    password VARCHAR
}

# comments table
CREATE TABLE comments {
    comment_id SERIAL PRIMARY KEY,
    user_id VARCAHR FOREIGN KEY REFERENCES users.user_id,
    zipcode INTEGER,
    comment VARCHAR
}

# END database structures
# -----------------------------------------------------------


-- # inserting data into table
-- INSERT INTO locations
--     (zipcode, city, state, lat, lon, population)
--     VALUES( , ' ', ' ', , , );
--
-- INSERT INTO comments
--     (user_id, zipcode, comment)
--     VALUES('mcdomx', '02138', 'super nice place');
--
-- # selecting data from Database
-- SELECT * FROM locations; #selects all items from locations
-- SELECT lot, lon FROM locations WHERE city = "Boston" OR zip = "02138";
-- SELECT AVG(population) FROM locations WHERE lat > 45;
-- SELECT COUNT(*) FROM locations WHERE city = "Springfield";
-- SELECT * FROM locations WHERE city LIKE '%Spring%;' # '%' is wildcard
--
-- # updating table data
-- UPDATE comments
--     SET comment = 'really nice place'
--     WHERE comment_id = 1;

-- # nested queries
-- SELECT * FROM flights WHERE id IN
-- (SELECT flight_id FROM passengers GROUP BY flight_id HAVING COUNT(*) > 1)

-- locking database using SQL Transactions
BEGIN
COMMIT

-- SQL Alchemy: python module that enables SQL Transactions
from sqlalchemy import create_engine
from sqlaclchemy.orm import scoped_session, sessionmaker
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

-- pthon commands for sql commands
flights = db.execute("SELECT * FROM flights").fetchall()  #fetchone() will only get one result
-- flights becomes an interbale object so 'for flight from flights' can be used
-- db.execute returns that results of the query
-- elements can be referenced by flight.flight_id.
