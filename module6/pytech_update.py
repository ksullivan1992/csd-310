"""
Kyle Sullivan
Module 6.3
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

# Display the message telling the user that the program is updating a record and print the results
print("\n****** Displaying the updated student record in the collection ******\n")

# Update the specified student ID
result = students.update_one({"student_id": "1007"}, {"$set": {"last_name": "Skywalker"}})

# Find the updated record and set it to a variable
updated_result = students.find_one({"student_id": "1007"})

# Print out the updated student record
print("  Student ID: " + updated_result["student_id"] + "\n  First Name: " + updated_result["first_name"] + "\n  Last Name: " + updated_result["last_name"] + "\n")

# Exit message
input("\n\n  End of program, press any key to exit... ")
