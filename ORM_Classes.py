from flask import Flask, render_template, request, redirect, url_for
import sqlite3


# Authors Table ------------------------
class AuthorClass:
    def __init__(self, authorId, firstname, lastname):
        self.authorId = authorId
        self.firstname = firstname
        self.lastname = lastname

    # ORM get id given name
    #def get_id_from_name(self, fname, last):

    # ORM insert
    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert row with passed values
        cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?)',
                       (self.authorId, self.firstname, self.lastname))

        conn.commit()
        cursor.close()
        conn.close()


# Books Table ------------------------
class BookClass:
    def __init__(self, bookId, name, authorId, genre, ave_rating=None):
        self.bookId = bookId
        self.name = name
        self.authorId = authorId
        self.genre = genre
        self.ave_rating = ave_rating

    # ORM select matching ID
    def get_book_with_id(bookid):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Find book
        cursor.execute('SELECT * FROM Books WHERE bookId = ?;', (bookid,))

        result = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        if result:
            # Create an instance of BookClass
            obj = BookClass(*result)
            return obj
        else:
            return None

    # ORM update book's info - CANNOT update rating this way
    def update_book_data(self, name, authorfirstname, authorlastname, genre):

        self.name = name
        self.genre = genre

        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE Books SET name = ?, genre = ? WHERE bookId  = ?', (self.name, self.genre, self.bookId))

        conn.commit()
        cursor.close()
        conn.close()



    # ORM insert
    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert passed data
        cursor.execute('INSERT INTO Books (bookId, name, authorId, genre, ave_rating)  VALUES (?, ?, ?, ?, ?);',
                       (self.bookId, self.name, self.authorId, self.genre, self.ave_rating))

        conn.commit()
        cursor.close()
        conn.close()


# Users Table ------------------------
class UserClass:
    def __init__(self, userId, username, password):
        self.userId = userId
        self.username = username
        self.password = password

    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert passed data
        cursor.execute('INSERT INTO Users (userId, username, password)  VALUES (?, ?, ?);',
                       (self.userId, self.username, self.password))

        conn.commit()
        cursor.close()
        conn.close()


# Ratings Table ------------------------
class RatingClass:
    def __init__(self, ratingId, userId, bookId, rating):
        self.ratingId = ratingId
        self.userId = userId
        self.bookId = bookId
        self.rating = rating

    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert passed data
        cursor.execute('INSERT INTO Ratings (ratingId, userId, bookId, rating)  VALUES (?, ?, ?, ?);',
                       (self.ratingId, self.userId, self.bookId, self.rating))

        conn.commit()
        cursor.close()
        conn.close()

        print("saved new rating for book, recalc now")
        self.recalculate_ratings()

    def recalculate_ratings(self):
        # recalculates the ave rating for the book whose rating is being edited, deleted, or added
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # get all ratings for that book
        cursor.execute('SELECT rating FROM Ratings bookId WHERE bookId = ?;', (self.bookId,))
        results = cursor.fetchall()

        new_ave = 0;
        if (results is not None):

            for res in results:
                new_ave += res[0]
            new_ave /= len(results)
        else:
            # book is now unrated
            new_ave = None

        # update book with new average rating
        cursor.execute('UPDATE Books SET ave_rating = ? WHERE bookId  = ?', (new_ave, self.bookId))

        conn.commit()
        cursor.close()
        conn.close()