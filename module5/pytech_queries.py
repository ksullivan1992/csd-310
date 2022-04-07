"""
Kyle Sullivan
Module 5.3
6/7/2022
"""

# Import the Mongo DB package
from pymongo import MongoClient

# Create the url for the db connection
url = "mongodb+srv://admin:admin@cluster0.dkpqp.mongodb.net/pytech"

# Create the db connection object
client = MongoClient(url)

# Connect to the DB
db = client.pytech

students = db.students

student_list = students.find({})

print("\n -- DISPLAYING STUDENT DOCUMENTS FROM .find() THE QUERY --")

for doc in student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

obiwan = students.find_one({"student_id": "1008"})

# output the results 
print("\n  -- DISPLAYING STUDENT DOCUMENT FROM find_one() QUERY --")
print("  Student ID: " + obiwan["student_id"] + "\n  First Name: " + obiwan["first_name"] + "\n  Last Name: " + obiwan["last_name"] + "\n")

# exit message 
input("\n\n  End of program, press any key to continue...")
