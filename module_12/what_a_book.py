""" 
Kyle Sullivan
Module 12 What_a_book
5/10/2022
"""

""" import statements """
from calendar import c
import sys
import mysql.connector
from mysql.connector import errorcode


""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}


# Shows the main menu to the user
def show_menu():
    print("\n\n          -- Main Menu --")

    print("          1: View Books\n          2: View Store Locations\n          3: My Account\n          4: Exit Program\n")

    try:
        choice = int(input('          Enter an option >>>> '))
        return choice

    except ValueError:
        print("\n  Invalid number! Program exiting, please try again...\n")
        sys.exit(0)


# Shows the book list to the user
def show_books(_cursor):
    # DB query
    _cursor.execute("SELECT book_id, book_name, author, details FROM book")

    books = _cursor.fetchall()

    # Loop through and list all the records found
    print("\n\n  -- DISPLAYING BOOK LISTING --")
    for book in books:
        print("  Book Name: {}\n  Author: {}\n  Details: {}\n".format(book[0], book[1], book[2]))


# Shows the location of the book to the user
def show_locations(_cursor):
    # Db query
    _cursor.execute("SELECT store_id, locale from store")

    locations = _cursor.fetchall()

    print("\n\n  -- DISPLAYING STORE LOCATIONS --")
    for location in locations:
        print("  Locale: {}\n".format(location[1]))


# Validates the user ID and exits the program if it fails
def validate_user(_cursor):

    # Validate the users ID
    try:
        user_id = int(input('\n          Enter a customer id >> '))

        if user_id < 0 or user_id > 3:
            print("\n  Invalid customer number! Program exiting...\n")
            sys.exit(0)

        _cursor.execute("SELECT first_name, last_name "
                        "FROM user "
                        "WHERE user_id = {}".format(user_id))

        user = _cursor.fetchall()

        for user_info in user:
            print("\nUSER VALIDATED\nWelcome {} {}!".format(user_info[0], user_info[1]))

        return user_id

    except ValueError:
        print("\n  Invalid number! Program exiting...\n")

        sys.exit(0)


# Shows the users account information
def show_account_menu():

    # display the users account menu
    try:
        print("\n\n          -- Customer Menu --")
        print("          1. Wishlist\n          2. Add Book\n          3. Remove Book\n          4. Main Menu")
        account_option = int(input('          Enter an option >>>> '))

        return account_option

    except ValueError:
        print("\n  Invalid number! Program exiting...\n")

        sys.exit(0)


# Shows the customer wishlist
def show_wishlist(_cursor, _user_id):

    # Queries the database for a list of books added to the users wishlist
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    
    wishlist = _cursor.fetchall()

    print("\n\n  -- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist:
        print("Book Id: {}\nBook Name: {}\nAuthor: {}\n".format(book[3], book[4], book[5]))


# Shows the books that are available to add to the wishlist that are not currently there
def show_books_to_add(_cursor, _user_id):

    query = ("SELECT book_id, book_name, author "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n\n  -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("Book Id: {}\nBook Name: {}\n".format(book[0], book[1]))


# Adds a book to the users wishlist
def add_book_to_wishlist(_cursor, _user_id, _book_id):

    # Get all books that are currently in the users wishlist
    _cursor.execute("SELECT book_id, book_name, author, details "
                    "FROM book "
                    "WHERE book_id = {}".format(_book_id))
    
    wishlist = _cursor.fetchall()

    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))

    for removed_book in wishlist:
        print("\nBook ID: {}\n{}\n{}\nAdded to wishlist!\n".format(removed_book[0], removed_book[1], removed_book[3]))


# Removes a book from the users wishlist
def remove_book_from_wishlist(_cursor, _user_id, _book_id):

    # Get all books that are currently in the users wishlist
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {} AND book.book_id = {}".format(_user_id, _book_id))
    
    wishlist = _cursor.fetchall()

    _cursor.execute("DELETE FROM wishlist WHERE book_id = {}".format(_book_id))

    for removed_book in wishlist:
        print("\nBook ID: {}\n{}\n{}\nRemoved from wishlist!\n".format(removed_book[3], removed_book[4], removed_book[5]))


# ** Main program **
try:
    db = mysql.connector.connect(**config) # connect to the WhatABook database 
    cursor = db.cursor() # cursor for MySQL queries

    print("\n\n\nWelcome to the WhatABook Store!!\nPlease select an option below")

    # Shows the main menu
    user_selection = show_menu() 

    while user_selection != 4:

        # Show books if user selection is 1
        if user_selection == 1:
            show_books(cursor)

        # Show the locations if the user selection is 2
        if user_selection == 2:
            show_locations(cursor)

        # If user selection is 3, validate user, then show the account menu
        if user_selection == 3:
            my_user_id = validate_user(cursor)
            account_option = show_account_menu()

            # Exit when the user selects option 4 by setting the boolean 'exit' to True, otherwise continue into this loop
            exit = False
            while exit != True:

                # Shows the users wishlist if they select option 1 
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                # Allows the user to enter another menu if they select option 2 to view and add a book to their wishlist
                if account_option == 2:

                    # Show all books not in the users wishlist
                    show_books_to_add(cursor, my_user_id)

                    # Allows the user to select a wishlist item
                    book_id = int(input("\n        Enter the id of the book to add >> "))
                    
                    # Adds the selected book to the wishlist
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    # Commit changes to the database 
                    db.commit()

                # Allow the user to log into their account
                if account_option == 3:

                    # Shows the user wishlist
                    show_wishlist(cursor, my_user_id)

                    # Allows the user to select a book ID to remove
                    remove_id = int(input("\n          Enter the ID of the book to remove >> "))

                    # Calls the remove book function
                    remove_book_from_wishlist(cursor, my_user_id, remove_id)

                    # Commit changes to the database
                    db.commit()

                # Print out a message and exit to main menu
                if account_option == 4:

                    print("Goodbye!\n\nExiting to Main Menu")
                    exit = True

                # Resets the user to the menu if they choose an option that is out of bounds
                if account_option < 0 or account_option > 4:
                    print("\n  Invalid option! Please try again...")

                # Shows the account menu again if user did not exit
                if account_option != 4:

                    # Show the account menu
                    account_option = show_account_menu()
        
        # if the user selection is less than 0 or greater than 4, display an invalid user selection
        if user_selection < 0 or user_selection > 4:
            print("\n      Invalid option, please retry...")
            
        # Show the main menu
        user_selection = show_menu()

    print("\n\n  Program exiting...")

except mysql.connector.Error as err:
    """ handle errors """ 

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()
