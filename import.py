# This module will load data from zips.csv into the application's database

import platform

def main():
        # Ask user for confirmation
        # WARNING: all application table data will be erased
        message("WARNING: All application's database tables will be erased.")
        message("Confirm. Do you want to ERASE and recreate the application database.(Y/N)")
        response = input()
        if response is 'N':
            exit(0)
        # TODO: If tables exist, delete theme
        # Run database_setup.psql
        # Open zips.csv file
        # Skip first line of file
        # loop through lines of the file and INSERT each one into locations tables
        # close file

if __name__ == '__main__': main()
