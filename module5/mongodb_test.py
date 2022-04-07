"""
Kyle Sullivan
Module 5.2
4/7/2022
"""

# Import the Mongo DB package
from pymongo import MongoClient

# Create the url for the db connection
url = "mongodb+srv://admin:admin@cluster0.dkpqp.mongodb.net/pytech"

# Create the db connection object
client = MongoClient(url)

# Connect to the DB
db = client.pytech

# Print out the collection names in the db
print("\n -- Pytech COllection List --")
print(db.list_collection_names())

input("\n\n  End of program, press any key to exit... ")
