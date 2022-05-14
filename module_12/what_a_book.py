""" 
Kyle Sullivan
Module 12 What_a_book
5/14/2022
"""

# Import statements
import sys
import mysql.connector
from mysql.connector import errorcode


# Database config object
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
        # User enters an option
        user_selection = int(input('          Enter an option >>>> '))

        # Show books if user selection is 1
        if user_selection == 1:
            show_books(cursor)
            show_menu()

        # Show the locations if the user selection is 2
        if user_selection == 2:
            show_locations(cursor)
            show_menu()

        # If user selection is 3, validate user, then show the account menu
        if user_selection == 3:
            
            try:
                # User enters a user ID
                user_id = int(input('\n          Enter a customer id >> '))

                # If the user_id is 0-3, execute this code, otherwise present the menu again with a message
                if user_id > 0 and user_id < 4:
                    validate_user(cursor, user_id)
                    show_account_menu(user_id)

                else:
                    print("\n  Invalid entry! Please try again!\n")
                    user_selection = show_menu()

            except (ValueError, TypeError):
                print("\n  Invalid entry! Please try again!\n")
                user_selection = show_menu()

            show_menu()

        if user_selection == 4:
            print("\n\nThank you for using WHAT_A_BOOK! Exiting...\n\n")
            sys.exit(0)

        try:
            # if the user selection is less then 0 or greater than 4, execute this code and present the menu again with a message
            if user_selection < 0 or user_selection > 4:
                print("\n      Invalid entry! Please try again!")
        
                # Show the main menu
                user_selection = show_menu()

        except (TypeError, ValueError):
            print("\n      Invalid entry! Please try again!")
            user_selection = show_menu()

    except (ValueError, TypeError):
        print("\n      Invalid entry! Please try again!")
        user_selection = show_menu()


# Shows the book list to the user
def show_books(cursor):

    # DB query
    cursor.execute("SELECT book_id, book_name, author, details FROM book")

    books = cursor.fetchall()

    # Loop through and list all the records found
    print("\n\n  -- DISPLAYING BOOK LISTING --")
    for book in books:
        print("  Book Name: {}\n  Author: {}\n  Details: {}\n".format(book[1], book[2], book[3]))


# Shows the location of the book to the user
def show_locations(cursor):

    # Db query
    cursor.execute("SELECT store_id, locale from store")

    locations = cursor.fetchall()

    # Display all the store locations
    print("\n\n  -- DISPLAYING STORE LOCATIONS --")
    for location in locations:
        print("  Locale: {}\n".format(location[1]))


# Validates the user ID
def validate_user(cursor, user_id):

    # Validate the users ID
    cursor.execute("SELECT first_name, last_name "
                    "FROM user "
                    "WHERE user_id = {}".format(user_id))

    user = cursor.fetchall()

    # Print out the verification message
    for user_info in user:
        print("\nUSER VALIDATED\nWelcome {} {}!".format(user_info[0], user_info[1]))


# Shows the customer wishlist
def show_wishlist(cursor, user_id):

    # Queries the database for a list of books added to the users wishlist
    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(user_id))
    
    wishlist = cursor.fetchall()

    # Display the wishlist items
    print("\n\n  -- DISPLAYING WISHLIST ITEMS --")
    for book in wishlist:
        print("Book Id: {}\nBook Name: {}\nAuthor: {}\n".format(book[3], book[4], book[5]))


# Shows the books that are available to add to the wishlist that are not currently there
def show_books_to_add(cursor, user_id):

    query = ("SELECT book_id, book_name, author "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(user_id))

    cursor.execute(query)

    books_to_add = cursor.fetchall()

    # Display all the available books that are not in the current wishlist
    print("\n\n  -- DISPLAYING AVAILABLE BOOKS --")
    for book in books_to_add:
        print("Book Id: {}\nBook Name: {}\n".format(book[0], book[1]))


# Adds a book to the users wishlist
def add_book_to_wishlist(cursor, user_id, book_id):

    try:

        # If the book_id is 1-9, add the book, otherwise display an error message and return to the customer menu
        if book_id > 0 and book_id < 10:

            # Get all books that are currently in the users wishlist
            cursor.execute("SELECT book_id, book_name, author, details "
                            "FROM book "
                            "WHERE book_id = {}".format(book_id))
            
            wishlist = cursor.fetchall()

            cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(user_id, book_id))

            # Display a confirmation message
            for removed_book in wishlist:
                print("\nBook ID: {}\n{}\n{}\nAdded to wishlist!\n".format(removed_book[0], removed_book[1], removed_book[3]))

        else:
            print("\n  Invalid entry! Please try again!\n")
            show_account_menu(user_id)

    except (ValueError, TypeError):
        print("\n  Invalid entry! Please try again!\n")
        show_account_menu(user_id)


# Removes a book from the users wishlist
def remove_book_from_wishlist(cursor, user_id, book_id):

    try:

        # If the book_id is 1-9, remove the book, otherwise display an error message and return to the customer menu
        if book_id > 0 and book_id < 10:

            # Get all books that are currently in the users wishlist
            cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author "
                            "FROM wishlist "
                            "INNER JOIN user ON wishlist.user_id = user.user_id "
                            "INNER JOIN book ON wishlist.book_id = book.book_id "
                            "WHERE user.user_id = {} AND book.book_id = {}".format(user_id, book_id))
            
            wishlist = cursor.fetchall()

            cursor.execute("DELETE FROM wishlist WHERE book_id = {}".format(book_id))

            # Display a confirmation message
            for removed_book in wishlist:
                print("\nBook ID: {}\n{}\n{}\nRemoved from wishlist!\n".format(removed_book[3], removed_book[4], removed_book[5]))
        
        else:
            print("\n  Invalid entry! Please try again!\n")
            show_account_menu(user_id)

    except (ValueError, TypeError):
        print("\n  Invalid entry! Please try again!\n")
        show_account_menu(user_id)


# Shows the users account information
def show_account_menu(user_id):

    # Display the users account menu
    try:
        print("\n\n          -- Customer Menu --")
        print("          1. Wishlist\n          2. Add Book\n          3. Remove Book\n          4. Main Menu")

        account_option = int(input('          Enter an option >>>> '))

        # Return to the customer menu if the user selects an option outside the displayed options
        if account_option > 0 and account_option < 5:
            customer_menu(account_option, user_id)

        else:
            print("\n  Invalid entry! Please try again!\n")
            show_account_menu(user_id)

    except (ValueError, TypeError):
        print("\n  Invalid entry! Please try again!\n")
        show_account_menu(user_id)


def customer_menu(account_option, user_id):

    # Exit when the user selects option 4 by setting the boolean 'exit' to True, otherwise continue into this loop
    exit = False
    while exit != True:

        # Shows the users wishlist if they select option 1 
        if account_option == 1:
            show_wishlist(cursor, user_id)
            show_account_menu(user_id)

        # Allows the user to enter another menu if they select option 2 to view and add a book to their wishlist
        if account_option == 2:

            # Show all books not in the users wishlist
            show_books_to_add(cursor, user_id)

            # Allows the user to select a wishlist item
            book_id = int(input("\n        Enter the id of the book to add >> "))
            
            # Adds the selected book to the wishlist
            add_book_to_wishlist(cursor, user_id, book_id)

            # Commit changes to the database 
            db.commit()

            show_account_menu(user_id)

        # Allow the user to log into their account
        if account_option == 3:

            # Shows the user wishlist
            show_wishlist(cursor, user_id)

            # Allows the user to select a book ID to remove
            remove_id = int(input("\n          Enter the ID of the book to remove >> "))

            # Calls the remove book function
            remove_book_from_wishlist(cursor, user_id, remove_id)

            # Commit changes to the database
            db.commit()

            show_account_menu(user_id)

        # Print out a message and exit to main menu
        if account_option == 4:

            # Display a goodbye message
            print("Goodbye!\n\nExiting to Main Menu")
            exit = True
            show_menu()

        # Resets the user to the menu if they choose an option that is out of bounds
        if account_option < 0 or account_option > 4:
            print("\n  Invalid option! Please try again...")

        # Shows the account menu again if user did not exit
        if account_option != 4:

            # Show the account menu
            account_option = show_account_menu()



# ****** MAIN PROGRAM ******
try:
    # Connect to the WhatABook database 
    db = mysql.connector.connect(**config)

    # Cursor for MySQL queries
    cursor = db.cursor()

    # Display the welcome message
    print("\n\n\nWelcome to the WhatABook Store!!\nPlease select an option below")

    # Shows the main menu
    show_menu()

# Error handling on the mysql db connection
except mysql.connector.Error as err:

    # Handle errors
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:

   # Close the connection to MySQL
    db.close()
