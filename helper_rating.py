from flask import Flask, render_template, request, redirect, url_for
import sqlite3


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