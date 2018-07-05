# This module will load data from zips.csv into the application's database

import platform
import os
import csv
from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey, Sequence
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
                delete_tables()
                setup_tables();
                load_tables();
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
    metadata = MetaData()
    tables = ['tbl_comments', 'tbl_users', 'tbl_locations']
    # tables = ['tbl_comments','tbl_users']
    for table in tables:
        selected_table = Table(table, metadata)
        if selected_table.exists(engine):
            selected_table.drop(engine)
            print(f"- Table '{table}' deleted")
        else:
            print(f"Table '{table}' does not exist")

def setup_tables():
    setup_locations_table()
    setup_users_table()
    setup_comments_table()

def setup_locations_table():
    metadata = MetaData()
    locations = Table('tbl_locations', metadata,
        Column('zipcode', String, primary_key=True),
        Column('city', String, nullable=False),
        Column('state', String, nullable=False),
        Column('lat', Float, nullable=False),
        Column('lon', Float, nullable=False),
        Column('population', Integer, nullable=False)
    )
    metadata.create_all(engine)
    print("+ Table 'tbl_locations' created.")

def setup_users_table():
    metadata = MetaData()
    locations = Table('tbl_users', metadata,
        Column('user_id', String, primary_key=True),
        Column('name', String, nullable=False),
        Column('password', String, nullable=False)
    )
    metadata.create_all(engine)
    print("+ Table 'tbl_users' created.")

def setup_comments_table():
    db.execute("CREATE TABLE tbl_comments (                     \
        comment_id SERIAL PRIMARY KEY,                          \
        user_id VARCHAR REFERENCES tbl_users,                   \
        zipcode VARCHAR REFERENCES tbl_locations,               \
        comment VARCHAR)")
    db.commit()
    print("+ Table 'tbl_comments' created.")

def load_tables():
    import_zips()
    import_users()
    import_comments()

def import_zips(csv_file="zips.csv"):
    f = open_file(csv_file)
    if f is None:
        return
    reader = csv.reader(f)
    i = 1

    for zip, city, st, lat, lon, pop in reader:
        if i>1:
            print(f"\rLoading record: {i}", end="")
            zip = str(zip)
            if len(zip) is 4:
                zip = "0"+zip
            db.execute("INSERT INTO tbl_locations (zipcode, city, state, lat, lon, population) VALUES (:Zipcode, :City, :State, :Lat, :Lon, :Population)",
                {"Zipcode":zip, "City":city, "State":st, "Lat":lat, "Lon":lon, "Population":pop})
        i += 1
    print("...Done")
    print("Committing to database...")
    db.commit()
    print("Data committed.  Data load complete.")
    f.close()

def import_users(csv_file="users.csv"):
    f = open_file(csv_file)
    if f is None:
        return
    reader = csv.reader(f)
    i = 1
    for user, name, pw in reader:
        if i>1:
            print(f"\rLoading record: {i}", end="")
            db.execute("INSERT INTO tbl_users (user_id, name, password) VALUES (:UID, :Name, :PW)",
                {"UID":user, "Name":name, "PW":pw})
        i += 1
    print("...Done")
    print("Committing to database...")
    db.commit()
    print("Data committed.  Data load complete.")
    f.close()

def import_comments(csv_file="comments.csv"):
    f = open_file(csv_file)
    if f is None:
        return
    reader = csv.reader(f)
    i = 1
    for user, zip, comment in reader:
        if i>1:
            print(f"\rLoading record: {i}", end="")
            db.execute("INSERT INTO tbl_comments (comment_id, user_id, zipcode, comment) VALUES (:CID, :UID, :Zip, :Comment)",
                {"CID":i , "UID":user, "Zip":zip, "Comment":comment})
        i += 1
    print("...Done")
    print("Committing to database...")
    db.commit()
    print("Data committed.  Data load complete.")
    f.close()

def open_file(file_name):
    f = open(file_name)
    if f is None:
        print(f"File '{csv_file}' not found.")
        return None
    else:
        print(f"Loading data from {file_name}...")
        return f

if __name__ == '__main__': main()
