"""
Kyle Sullivan
Module 8.3
4/19/2022
"""

# Import the Mongo DB package
import mysql.connector
from mysql.connector import errorcode
from pymongo import MongoClient

# Create the url for the db connection
url = "mongodb+srv://admin:admin@cluster0.dkpqp.mongodb.net/pytech"

# Create the db connection object
client = MongoClient(url)

# Connect to the DB
db = client.pytech

# Create the config varable with connection data
config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the pysports database 

    cursor = db.cursor()

    # Execute the SQL query
    cursor.execute("SELECT team_id, team_name, mascot FROM team")

    # Get all the entires for the teams table
    teams = cursor.fetchall()

    print("\n  -- DISPLAYING TEAM RECORDS --")

    # Iterate over the records in the team table and print the results
    for team in teams: 
        print("  Team ID: {}\n  Team Name: {}\n  Mascot: {}\n".format(team[0], team[1], team[2]))

    # Execute the query
    cursor.execute("SELECT player_id, first_name, last_name, team_id FROM player")

    # Get all the player table records
    players = cursor.fetchall()

    print("\n  -- DISPLAYING PLAYER RECORDS --")

    # Iterate over the player table and print the results
    for player in players:
        print("  Player ID: {}\n  First Name: {}\n  Last Name: {}\n  Team ID: {}\n".format(player[0], player[1], player[2], player[3]))

    # End of program
    input("\n\n  End of program, press any key to exit... ")

# If connection errors, print error
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")

    else:
        print(err)

# Whether or not the connection works, close the DB connection
finally:
    db.close()

