import datetime

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    success = False
    return render_template('main_page.html', success=success)

# @app.route('/', methods=['POST', 'GET'])
def reset_database():
    # Change to stored procedure?
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS Books;')
    cursor.execute('DROP TABLE IF EXISTS Authors;')

    # Create Authors(authorId, firstname, lastname, birth_year, death_year)
    cursor.execute('CREATE TABLE IF NOT EXISTS Authors '
                   '(authorId INTEGER PRIMARY KEY, '
                   'firstname TEXT, '
                   'lastname TEXT);')

    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (1, "Leigh", "Bardugo"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (2, "Neil", "Gaiman"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (3, "William", "Shakespeare"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (4, "Agatha", "Christie"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (5, "Madeline", "Miller"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (6, "Robert", "Frost"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (7, "Stephen", "King"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (8, "Michelle", "Obama"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (9, "Kevin", "Kwan"))
    cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (10, "Robin", "Kimmerer"))

    # Create Books(bookId, name, authorId, genre, length_in_pages)
    cursor.execute('CREATE TABLE IF NOT EXISTS Books '
                   '(bookId INTEGER PRIMARY KEY, '
                   'name TEXT, '
                   'authorId INTEGER, '
                   'genre TEXT, '
                   'FOREIGN KEY(authorId) REFERENCES Authors(authorId));')

    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);', (1, "Six of Crows", 1, "Fantasy"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);', (2, "Coraline", 2, "Fantasy"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (3, "Romeo and Juliet", 3, "Play"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (4, "Murder on the Orient Express", 4, "Mystery"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (5, "The Song of Achilles", 5, "Historical Fiction"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (6, "The Road Not Taken", 6, "Poetry"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (7, "It", 7, "Horror"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (8, "Becoming", 8, "Autobiography"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (9, "Crazy Rich Asians", 9, "Romance"))
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                   (10, "Braiding Sweetgrass", 10, "Contemporary"))
    conn.commit()
    return

@app.route('/', methods=['POST', 'GET'])
def update_database():
    success = False
    bookname = request.form['newbook_input']
    bookauthorfirst = request.form['newauthorfirst_input']
    bookauthorsecond = request.form['newauthorsecond_input']
    bookgenre = request.form['newgenre_input']


    # Connect to the database
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    # Add to database using the user's input

    cursor.execute('SELECT max(bookId) from Books;')

    # Calculate a new book ID
    result = cursor.fetchone()
    if (result[0] is None):
        max_id = 1
    else:
        max_id = result[0] + 1

    # Calculate author's id
    ## SANITIZE INPUT TO AVOID SQL INJECTION ATTACKS
    cursor.execute('SELECT authorId FROM Authors a WHERE a.firstname = ? AND a.lastname = ?', (bookauthorfirst, bookauthorsecond))
    results = cursor.fetchone()
    aId = 0

    if (result[0] is None):
        # New author, need to add to the Authors table

        # Calculate a new author ID
        cursor.execute('SELECT max(authorId) from Authors;')
        result = cursor.fetchone()
        if (result[0] is None):
            aId = 1
        else:
            aId = result[0] + 1

        # Add new author
        cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);',
                       (aId, bookauthorfirst, bookauthorsecond))
    else:
        aId = results[0]

    # Check for existing book

    # id, name, genre, author, length
    cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);', (max_id, bookname, aId, bookgenre))
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
    # reset_database()
    app.run(debug=True)