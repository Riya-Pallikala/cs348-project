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
        # immediate locks, no preprocessing so should not cause delays,
        # and want Authors table to be consistent due to foreign key dependency in Books

        conn = sqlite3.connect('databases/test_db1.db', isolation_level="IMMEDIATE")
        cursor = conn.cursor()

        # Insert row with passed values
        cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?)',
                       (self.authorId, self.firstname, self.lastname))

        conn.commit()
        cursor.close()
        conn.close()


# Books Table ------------------------
class BookClass:
    def __init__(self, bookId, name, authorId, genre, ave_rating='None'):
        self.bookId = bookId
        self.name = name
        self.authorId = authorId
        self.genre = genre
        self.ave_rating = ave_rating

    # ORM select matching ID
    def get_book_with_id(bookid):
        # immediate locks, no preprocessing so should not cause delays,
        # only doing a read, so locking will not block other reads
        # but still want to get a read lock, to make sure we don't say a book doesn't exist when it does or vice versa
        # ie. don't want to allow deletion to concurrently execute

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE')
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

    # ORM update book's info - CANNOT update ave rating directly this way, must use Rating Class defs
    def update_book_data(self, genre):
        self.genre = genre

        # immediate locks, no preprocessing so should not cause delays,
        # would prefer to update genre before allowing reads to ensure updated data

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE')
        cursor = conn.cursor()

        cursor.execute('UPDATE Books SET genre = ? WHERE bookId  = ?', (self.genre, self.bookId))

        conn.commit()
        cursor.close()
        conn.close()



    # ORM insert
    def save_to_db(self):
        # immediate locks, no preprocessing so should not cause delays,
        # and want Books table to be consistent due to foreign key dependency in Ratings

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE')
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
        # immediate locks, no preprocessing so should not cause delays,
        # and want Users table to be consistent due to foreign key dependency in Ratings,
        # and enforce unique usernames across all users (two users shouldn't create at the exact same time)

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE')
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
        # deferred locks, but not much difference here due to only one insert
        # Ratings is not referenced by anything, and it is ok for ratings data to be slightly outdated

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='DEFERRED')
        cursor = conn.cursor()

        # Insert passed data
        cursor.execute('INSERT INTO Ratings (ratingId, userId, bookId, rating)  VALUES (?, ?, ?, ?);',
                       (self.ratingId, self.userId, self.bookId, self.rating))

        conn.commit()
        cursor.close()
        conn.close()

        # print("saved new rating for book, recalc now")
        self.recalculate_ratings()

    # ORM select matching ID
    def get_ratingid_given_user_and_book(userId, bookId):
        # read, so can defer; wait to get read lock in case other changes are being made still
        conn = sqlite3.connect('databases/test_db1.db', isolation_level='DEFERRED')
        cursor = conn.cursor()

        # Find book
        cursor.execute('SELECT * FROM Ratings WHERE userId =? AND bookId = ?;', (userId, bookId))

        result = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        if result:
            # Create an instance of BookClass
            obj = RatingClass(*result)
            return obj
        else:
            return None

    # ORM update book's info - CANNOT update ave rating this way
    def update_rating_data(self, rating):

        self.rating = rating

        # write, but can defer;
        # wait to get lock in case other changes are being made still;
        # ie. maybe another user is updating their own rating, so recalculate should be performed after anyways
        # and if user is updating from two different tabs, then the latter one should be applied, so no need
        # to block the earlier if it occurs after this transaction starts

        conn = sqlite3.connect('databases/test_db1.db', )
        cursor = conn.cursor()

        cursor.execute('UPDATE Ratings SET rating = ? WHERE ratingId  = ?',
                       (self.rating, self.ratingId))

        conn.commit()
        cursor.close()
        conn.close()

        self.recalculate_ratings()

    def recalculate_ratings(self):

        # recalculates the ave rating for the book whose rating is being edited, deleted, or added

        # immediately lock , as we are reading and then writing data based on the read, want to be consistent

        conn = sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE')
        cursor = conn.cursor()

        # get all ratings for that book
        cursor.execute('SELECT rating FROM Ratings bookId WHERE bookId = ?;', (self.bookId,))
        results = cursor.fetchall()

        new_ave = 0;
        if (results is not None and results != '' and len(results) > 0):

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
        return