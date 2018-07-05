# This module will load data from zips.csv into the application's database

import platform
import os
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
    metadata = MetaData()
    tables = ['locations', 'comments', 'users']
    for table in tables:
        selected_table = Table(table, metadata)
        if selected_table.exists(engine):
            selected_table.drop(engine)
            print(f"..Table '{table}' deleted")
        else:
            print(f"..Table '{table}' does not exist")

def setup_locations_table():
    metadata = MetaData()
    locations = Table('locations', metadata,
        Column('zipcode', String, primary_key=True),
        Column('city', String, nullable=False),
        Column('state', String, nullable=False),
        Column('lat', Float, nullable=False),
        Column('long', Float, nullable=False),
        Column('population', Integer, nullable=False)
    )
    metadata.create_all(engine)

def setup_users_table():
    metadata = MetaData()
    locations = Table('users', metadata,
        Column('user_id', String, primary_key=True),
        Column('name', String, nullable=False),
        Column('password', String, nullable=False)
    )
    metadata.create_all(engine)

def setup_comments_tableX():
    users_meta = MetaData()
    user_table = Table('users', users_meta)
    comments_meta = MetaData()
    locations = Table('comments', comments_meta,
        Column('comment_id', String, Sequence('seq', metadata=comments_meta), primary_key=True),
        Column('user_id', String, ForeignKey(user_table.user_id), nullable=False),
        Column('zipcode', String, nullable=False),
        Column('date', DateTime, onupdate=datetime.datetime.now),
        Column('comment', String, nullable=False)
    )
    metadata.create_all(engine)

def setup_comments_table():
    db.execute("CREATE TABLE comments (                         \
        comment_id SERIAL PRIMARY KEY,                          \
        user_id VARCHAR REFERENCES users,   \
        zipcode INTEGER,                                        \
        comment VARCHAR)")
    db.commit()

def setup_tables():
    setup_locations_table()
    setup_users_table()
    setup_comments_table()

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
