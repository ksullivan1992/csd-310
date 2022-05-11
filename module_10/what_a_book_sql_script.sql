/*
Kyle Sullivan
Module 12
5/10/2022
*/

-- drop test user if exists 
DROP USER IF EXISTS 'whatabook_user'@'localhost';

-- create whatabook_user and grant them all privileges to the whatabook database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

-- drop tables if they exist
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;

-- Create tables
CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    PRIMARY KEY(book_id)
);

-- Create users
CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

-- Create wishlist
CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_Id)
);

-- Insert store record 
INSERT INTO store(locale)
    VALUES('1000 Galvin Rd S, Bellevue, NE 68005');

-- Insert book records
INSERT INTO book(book_name, author, details)
    VALUES('Ahsoka', 'E.K. Johnston', 'Star Wars Ahsoka story');

INSERT INTO book(book_name, author, details)
    VALUES('Thrawn', 'Timothy Zahn', 'Star Wars Thrawn story');

INSERT INTO book(book_name, author, details)
    VALUES('Darth Plagueis', 'James Luceno', "Story about the downfall of Darth Plagueis the wise");

INSERT INTO book(book_name, author)
    VALUES('Shatterpoint', 'Matthew Stover');

INSERT INTO book(book_name, author)
    VALUES('Jedi Trial', 'Dan Cragg');

INSERT INTO book(book_name, author)
    VALUES('The Dark Lord Trilogy', 'James Luceno');

INSERT INTO book(book_name, author)
    VALUES('The Force Unleashed', 'Sean Williams');

INSERT INTO book(book_name, author)
    VALUES('The Han Solo Trilogy', 'A.C. Crispin');

INSERT INTO book(book_name, author)
    VALUES('Splinter Of the Minds Eye', 'Alan Dean Foster');

-- Insert Users
INSERT INTO user(first_name, last_name) 
    VALUES('Darth', 'Vader');

INSERT INTO user(first_name, last_name)
    VALUES('Luke', 'Skywalker');

INSERT INTO user(first_name, last_name)
    VALUES('Mace', 'Windu');

-- Insert Wishlists
INSERT INTO wishlist(user_id, book_id) 
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Darth'), 
        (SELECT book_id FROM book WHERE book_name = 'The Dark Lord Trilogy')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Luke'),
        (SELECT book_id FROM book WHERE book_name = 'The Han Solo Trilogy')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Mace'),
        (SELECT book_id FROM book WHERE book_name = 'Jedi Trial')
    );
