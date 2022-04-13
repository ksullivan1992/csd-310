"""
Kyle Sullivan
Module 6.2
4/13/2022
"""

# Import the Mongo DB package
from pymongo import MongoClient

# Create the url for the db connection
url = "mongodb+srv://admin:admin@cluster0.dkpqp.mongodb.net/pytech"

# Create the db connection object
client = MongoClient(url)

# Connect to the DB
db = client.pytech

# Get students collection
students = db.students

# Find all the students in the collection
student_list = students.find({})

# Print out the message to let the user know what its doing
print("\n****** Displaying all the students in the collection ******\n")

# Loop through and print all the records in the collection
for doc in student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

# New student record info
leia = {
    "student_id": "1010",
    "first_name": "Leia",
    "last_name": "Organa"
}

# Print out the message to let the user know what its doing
print("\n****** Displaying Insert Statement ******\n")

# Insert the new student into the students collection
inserted_student = students.insert_one(leia).inserted_id
print("Inserted student record Leia Organa into the students collection with document_id " + str(inserted_student))

# Find the new record and save it to a variable
leia_record = students.find_one({"student_id": "1010"})

# Print out the message to let the user know what its doing
print("\n****** Displaying the new student in the collection ******\n")

# Print out the updated student record
print("  Student ID: " + leia_record["student_id"] + "\n  First Name: " + leia_record["first_name"] + "\n  Last Name: " + leia_record["last_name"] + "\n")

# Delete the record in the collection
deleted_student = students.delete_one({"student_id": "1010"})

# Find all the students in the collection
student_list = students.find({})

# Print out the message to let the user know what its doing
print("\n****** Displaying all the students in the collection after deleting a record ******\n")

# Loop through and print all the records in the collection
for doc in student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

# Exit message
input("\n\n  End of program, press any key to exit... ")
