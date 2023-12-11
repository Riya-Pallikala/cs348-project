from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from ORM_Classes import AuthorClass

def get_authorid_from_name(bookauthorfirst, bookauthorsecond):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    aId = 0
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
    try:
        with sqlite3.connect('databases/test_db1.db', isolation_level='IMMEDIATE') as conn:
            cursor = conn.cursor()
            cursor.execute('BEGIN')

            aId = 0

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

    except Exception as e:
        # Rollback the transaction in case of an exception
        conn.rollback()

        # Log the exception or handle it as needed
        print(f"An error occurred when adding new Author: {str(e)}")
        return None

def get_full_author_name(author_id):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    cursor.execute('SELECT firstname, lastname FROM Authors WHERE authorId = ?', (author_id,))
    result = cursor.fetchone()

    conn.close()

    # Check if data is found
    if result:
        fullname = f"{result[0]} {result[1]}"
        return fullname
    else:
        return "Unknown Author"