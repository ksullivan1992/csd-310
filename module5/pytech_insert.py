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

""" three student documents"""
# Darth Vader's data document 
vader = {
    "student_id": "1007",
    "first_name": "Darth",
    "last_name": "Vader"
}

# Obiwan Kenobi data document 
obiwan = {
    "student_id": "1008",
    "first_name": "Obiwan",
    "last_name": "Kenobi"
}

# Mace Windu data document
mace = {
    "student_id": "1009",
    "first_name": "Mace",
    "last_name": "Windu"
}

students = db.students

# insert statements with output 
print("\n  -- INSERT STATEMENTS --")
vader_student_id = students.insert_one(vader).inserted_id
print("Inserted student record Darth Vader into the students collection with document_id " + str(vader_student_id))

obiwan_student_id = students.insert_one(obiwan).inserted_id
print("Inserted student record Obiwan Kenobi into the students collection with document_id " + str(obiwan_student_id))

mace_student_id = students.insert_one(mace).inserted_id
print("Inserted student record Mace Windu into the students collection with document_id " + str(mace_student_id))

input("\n\n  End of program, press any key to exit... ")
