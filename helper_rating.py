from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from ORM_Classes import RatingClass

def get_new_rating_id():
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    max_id = 0
    cursor.execute('SELECT max(ratingId) from Ratings;')
    result = cursor.fetchone()

    if (result is None or result[0] is None):
        # empty ratingList, this will be the first
        max_id = 1
    else:
        # increment largest ID by 1, will be unique ID
        max_id = result[0] + 1

    conn.commit()
    cursor.close()
    conn.close()
    return max_id

def delete_rating_with_user_and_book(userId, bookId):
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    tempRating = RatingClass.get_ratingid_given_user_and_book(userId, bookId)

    # delete from table

    if (tempRating is not None):
        cursor.execute("DELETE FROM Ratings WHERE bookId = ? AND userID = ?", (bookId, userId))
        conn.commit()
        cursor.close()
        conn.close()

        # use temp object to recalculate
        tempRating.recalculate_ratings()

    # else there is already no rating for that book from that user, just recalc for the book id
    recalculate_ratings_with_id(bookId)
    return

def delete_rating_with_book_only(bookId):
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # delete all rows from table with book
    cursor.execute("DELETE FROM Ratings WHERE bookId = ?", (bookId,))
    conn.commit()
    cursor.close()
    conn.close()

    # unlike delete_rating_with_user_and_book(), book no longer exists so no need to recalc ratings
    return

def recalculate_ratings_with_id(bookId):

    # recalculates the ave rating for the book whose id is passed in
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # get all ratings for that book
    cursor.execute('SELECT rating FROM Ratings bookId WHERE bookId = ?;', (bookId,))
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
    cursor.execute('UPDATE Books SET ave_rating = ? WHERE bookId  = ?', (new_ave, bookId))

    conn.commit()
    cursor.close()
    conn.close()
    return
