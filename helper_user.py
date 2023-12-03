from flask import Flask, render_template, request, redirect, url_for
import sqlite3


from ORM_Classes import UserClass


def validate_password(userId, given_pwd):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    uId = 0
    cursor.execute(
        'SELECT password FROM Users WHERE userId = ?',
        (userId,))

    result = cursor.fetchone()

    correct_pwd = result[0]


    cursor.close()
    conn.close()

    if correct_pwd != given_pwd:
        return 0
    else:
        return 1

def get_userid_from_username(uname):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    uId = 0
    cursor.execute(
        'SELECT userId FROM Users WHERE LOWER(username) = LOWER(?)',
        (uname,))

    result = cursor.fetchone()

    if (result is not None):
        uId = result[0]
    else:
        uId = None

    conn.commit()
    cursor.close()
    conn.close()

    return uId

def add_new_user(username, password):
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    cursor.execute('SELECT max(userId) from Users;')
    result = cursor.fetchone()
    if (result[0] is None):
        uId = 1
    else:
        uId = result[0] + 1

    # Add new author to Authors table
    newuser = UserClass(uId, username, password)
    newuser.save_to_db()

    conn.commit()
    cursor.close()
    conn.close()

    return uId
