from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from ORM_Classes import AuthorClass, BookClass, UserClass, RatingClass

from helper_author import *
from helper_book import *
from helper_rating import *

# Reset Database to default starting data
def reset_database():
    # Change to stored procedure?
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # drop tables to reset
    cursor.execute('DROP TABLE IF EXISTS Books;')
    cursor.execute('DROP TABLE IF EXISTS Authors;')
    cursor.execute('DROP TABLE IF EXISTS Users;')
    cursor.execute('DROP TABLE IF EXISTS Ratings;')

    # Create tables Authors(authorId, firstname, lastname)
    cursor.execute('CREATE TABLE IF NOT EXISTS Authors '
                   '(authorId INTEGER PRIMARY KEY, '
                   'firstname TEXT, '
                   'lastname TEXT);')

    # use ORM to insert each author instance
    newAuthor1 = AuthorClass(0, "Unknown", "Author")
    newAuthor1.save_to_db()

    newAuthor1 = AuthorClass(1, "Leigh", "Bardugo")
    newAuthor1.save_to_db()

    newAuthor2 = AuthorClass(2, "Neil", "Gaiman")
    newAuthor2.save_to_db()

    newAuthor3 = AuthorClass(3, "William", "Shakespeare")
    newAuthor3.save_to_db()

    newAuthor4 = AuthorClass(4, "Agatha", "Christie")
    newAuthor4.save_to_db()

    newAuthor5 = AuthorClass(5, "Madeline", "Miller")
    newAuthor5.save_to_db()

    newAuthor6 = AuthorClass(6, "Robert", "Frost")
    newAuthor6.save_to_db()

    newAuthor7 = AuthorClass(7, "Stephen", "King")
    newAuthor7.save_to_db()

    newAuthor8 = AuthorClass(8, "Michelle", "Obama")
    newAuthor8.save_to_db()

    newAuthor9 = AuthorClass(9, "Kevin", "Kwan")
    newAuthor9.save_to_db()

    newAuthor10 = AuthorClass(10, "Robin", "Kimmerer")
    newAuthor10.save_to_db()

    # Create Books(bookId, name, authorId, genre, length_in_pages)
    cursor.execute('CREATE TABLE IF NOT EXISTS Books '
                   '(bookId INTEGER PRIMARY KEY, '
                   'name TEXT, '
                   'authorId INTEGER, '
                   'genre TEXT, '
                   'ave_rating FLOAT,'
                   'FOREIGN KEY(authorId) REFERENCES Authors(authorId));')

    # use ORM to insert each author instance

    newBook1 = BookClass(1, "Six of Crows", 1, "Fantasy")
    newBook1.save_to_db()

    newBook1 = BookClass(2, "Coraline", 2, "Fantasy")
    newBook1.save_to_db()

    newBook1 = BookClass(3, "Romeo and Juliet", 3, "Play")
    newBook1.save_to_db()

    newBook1 = BookClass(4, "Murder on the Orient Express", 4, "Mystery")
    newBook1.save_to_db()

    newBook1 = BookClass(5, "The Song of Achilles", 5, "Historical Fiction")
    newBook1.save_to_db()

    newBook1 = BookClass(6, "The Road Not Taken", 6, "Poetry")
    newBook1.save_to_db()

    newBook1 = BookClass(7, "It", 7, "Horror")
    newBook1.save_to_db()

    newBook1 = BookClass(8, "Becoming", 8, "Autobiography")
    newBook1.save_to_db()

    newBook1 = BookClass(9, "Crazy Rich Asians", 9, "Romance")
    newBook1.save_to_db()

    newBook1 = BookClass(10, "Braiding Sweetgrass", 10, "Contemporary")
    newBook1.save_to_db()

    # create users and ratings tables - both empty
    cursor.execute('CREATE TABLE IF NOT EXISTS Users '
                   '(userId INTEGER PRIMARY KEY, username TEXT, password TEXT);')
    guestUser = UserClass(1, "guest", "guest")
    guestUser.save_to_db()

    cursor.execute('CREATE TABLE IF NOT EXISTS Ratings '
                   '(ratingId INTEGER PRIMARY KEY, '
                   'userId TEXT, '
                   'bookId INTEGER, '
                   'rating FLOAT, '
                   'FOREIGN KEY(userId) REFERENCES Users(userId),'
                   'FOREIGN KEY(bookId) REFERENCES Books(bookId));')

    create_indexes()

    conn.commit()
    cursor.close()
    conn.close()

    return



def create_indexes():
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # create index on author names
    cursor.execute('CREATE INDEX authorsNames ON Authors (firstname, lastname)');

    # create index on book ratings

    conn.commit()
    cursor.close()
    conn.close()