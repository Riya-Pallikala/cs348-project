from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from ORM_Classes import AuthorClass

def get_authorid_from_name(bookauthorfirst, bookauthorsecond):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    aId = 0
    """ cursor.execute(
        'SELECT authorId FROM Authors a WHERE LOWER(a.firstname) = LOWER(?) AND LOWER(a.lastname) = LOWER(?)',
        (bookauthorfirst.capitalize(), bookauthorsecond.capitalize())) """
    cursor.execute(
        'SELECT authorId FROM Authors a WHERE a.firstname = ? AND a.lastname = ?',
        (bookauthorfirst.capitalize(), bookauthorsecond.capitalize()))
    result = cursor.fetchone()

    if (result is not None):
        aId = result[0]
    else:
        aId = None

    conn.commit()
    cursor.close()
    conn.close()

    return aId

def add_new_author(bookauthorfirst, bookauthorsecond):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    cursor.execute('SELECT max(authorId) from Authors;')
    result = cursor.fetchone()
    if (result[0] is None):
        aId = 1
    else:
        aId = result[0] + 1

    # Add new author to Authors table
    newauthor = AuthorClass(aId, bookauthorfirst.capitalize(), bookauthorsecond.capitalize())
    newauthor.save_to_db()

    conn.commit()
    cursor.close()
    conn.close()

    return aId
def get_full_author_name(author_id):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # Assuming 'authors' is the name of your authors table
    cursor.execute('SELECT firstname, lastname FROM Authors WHERE authorId = ?', (author_id,))
    result = cursor.fetchone()

    conn.close()

    # Check if data is found
    if result:
        fullname = f"{result[0]} {result[1]}"
        return fullname
    else:
        return "Unknown Author"