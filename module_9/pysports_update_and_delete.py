"""
Kyle Sullivan
Module 9.2
4/19/2022
"""

# Import the Mongo DB package
import mysql.connector
from mysql.connector import errorcode

# Create the config varable with connection data
config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

def show_players(cursor, title):
    """
    Method to execute an inner join on the player and team table, 
    iterate over the dataset and output the results to the terminal window.
    """

    # inner join query 
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id")

    # get the results from the cursor object 
    players = cursor.fetchall()

    print("\n  -- {} --".format(title))
    
    # iterate over the player data set and display the results 
    for player in players:
        print("  Player ID: {}\n  First Name: {}\n  Last Name: {}\n  Team Name: {}\n".format(player[0], player[1], player[2], player[3]))

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the pysports database 

    # get the cursor object
    cursor = db.cursor()

    # insert player query 
    add_player = ("INSERT INTO player(first_name, last_name, team_id)"
                 "VALUES(%s, %s, %s)")

    # player data fields 
    player_data = ("Smeagol", "Shire Folk", 1)

    # insert a new player record
    cursor.execute(add_player, player_data)

    # commit the insert to the database 
    db.commit()

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER INSERT")

    # update the newly inserted record 
    update_player = ("UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = 'Smeagol'")

    # execute the update query
    cursor.execute(update_player)

    # commit the update to the database 
    db.commit()

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER UPDATE")

    delete_player = ("DELETE FROM player WHERE first_name = 'Gollum'")

    cursor.execute(delete_player)

    # commit the delete to the database 
    db.commit()

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER DELETE")

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