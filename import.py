# This module will load data from zips.csv into the application's database

import platform
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
        # Ask user for confirmation
        # WARNING: all application table data will be erased
        print("WARNING: All application's database tables will be erased.")
        print("Confirm. Do you want to ERASE and recreate the application database.(Y/N): ", end="")

        while( True ):
            response=get_Y_or_N()
            if response is 'Y':
                print("Deleting tables", end="")
                delete_tables()
                # setup_tables();
                # load_tables();
                break
            elif response is 'N':
                print("Exiting program.")
                exit(0)
            else:
                print("Respond with Y or N: ", end="")

# get a Y or N response from command line
# returns False if something else is typed
def get_Y_or_N():
    response=input()
    if response=='Y' or response=='N':
        return response
    else:
        return False


def delete_tables():
    db.execute("DROP TABLE locations")
    db.commit()

def setup_tables():
    db.execute("CREATE TABLE locations {zipcode VARCHAR PRIMARY KEY, city VARCHAR NOT NULL, state VARCHAR NOT NULL, lat FLOAT NOT NULL, long FLOAT NOT NULL, population INTEGER NOT NULL}")
    db.commit()

def load_tables():
    import_CSV("zips.csv")

def import_CSV(csv_file="zips.csv"):
    f = open(csv_file)
    reader = csv.reader(f) #moduel csv will enable reading csv format. reader become object to iterate
    # Skip first line of file
    # loop through lines of the file and INSERT each one into locations tables
    for z, c, s, lat, lon, pop in reader:
        db.execute("INSERT INTO locations (z, c, s, la, lo. pop) VALUES (:Zipcode, :City, :State, :Lat, :Long, :Population)",
            {"Zipcode":z, "City":c, "State":s, "Lat":la, "Long":lo, "Population":pop})
        db.commit()
    close(f)



if __name__ == '__main__': main()
