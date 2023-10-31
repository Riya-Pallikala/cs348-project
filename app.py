import datetime

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    success = False
    return render_template('main_page.html', success=success)

@app.route('/', methods=['POST', 'GET'])
def reset_database():
    # Change to stored procedure?
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    # Create Authors(authorId, firstname, lastname, birth_year, death_year)
    cursor.execute('CREATE TABLE IF NOT EXISTS Authors '
                   '(authorId INTEGER PRIMARY KEY, '
                   'firstname TEXT, '
                   'lastname TEXT);')

    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (1, "fname", "lname"))

    # Create Books(bookId, name, authorId, genre, length_in_pages)
    cursor.execute('CREATE TABLE IF NOT EXISTS Books '
                   '(bookId INTEGER PRIMARY KEY, '
                   'name TEXT, '
                   'authorId INTEGER, '
                   'genre TEXT, '
                   'FOREIGN KEY(authorId) REFERENCES Authors(authorId));')

@app.route('/', methods=['POST', 'GET'])
def update_database():
    success = False
    bookname = request.form['newbook_input']
    bookauthor = request.form['newauthor_input']
    bookgenre = request.form['newgenre_input']


    # Connect to the database
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    # Add to database using the user's input



    cursor.execute('SELECT max(bookId) from Books;')

    # Calculate a new ID
    result = cursor.fetchone()
    if (result[0] is None):
        max_id = 1
    else:
        max_id = result[0] + 1

    # Calculate author's id

    # Check for existing book

    # id, name, genre, author, length
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);', (max_id, bookname, 1, bookgenre))
    conn.commit()
    conn.close()

    success = True
    return render_template('main_page.html', success=success)

@app.route('/query', methods=['POST'])
def query_database():
    genre_input = request.form['genre_input']
    author_input = request.form['author_input']

    # Connect to the database
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    # Execute an SQL query using the user's input

    cursor.execute('SELECT * FROM Books;')
    result = cursor.fetchall()
    conn.close()

    # Process the result and return it to the user
    #if (len(result) == 0):
    #    return render_template('empty_results.html')

    return render_template('results.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)