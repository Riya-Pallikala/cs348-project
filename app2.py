import datetime

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from ORM_Classes import AuthorClass, BookClass, UserClass, RatingClass

from helper_author import *
from helper_book import *
from helper_rating import *
from helper_database import *

app = Flask(__name__)

# Handle only html page rendering and processing in this file
# ORM class logic abstracted to ORM_Classes.py
# Helper functions that are not Class defs abstracted to respectively named helper files
# Helper functions for general database setup abstracted to helper_database.py

# Home Page
@app.route('/')
def home():
    success = False
    return render_template('main_page.html', success=success)


# Add Book Form
@app.route('/', methods=['POST', 'GET'])
def update_database():
    success = False
    alreadyRegistered = False

    bookname = request.form['newbook_input']
    bookauthorfirst = request.form['newauthorfirst_input']
    bookauthorsecond = request.form['newauthorsecond_input']
    bookgenre = request.form['newgenre_input']
    bookrating = request.form['newrating_input']

    if bookauthorfirst == '':
        bookauthorfirst = "Unknown"
    if bookauthorsecond == '':
        bookauthorsecond = "Author"
    if bookgenre == '':
        bookgenre = "Unknown Genre"



    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # Add to database using the user's input


    # Calculate author's id
    aId = get_authorid_from_name(bookauthorfirst.capitalize(), bookauthorsecond.capitalize())

    if (aId is not None):
        # Author already exists, check that they don't already have a book of this name

        # Check for existing book in Books table
        cursor.execute('SELECT * FROM Books b WHERE b.authorId == ? AND LOWER(b.name) == LOWER(?)', (aId, bookname))
        result = cursor.fetchone()
        if (result is not None and result[0] is not None):
            # book already exists. Cannot register, so return failure message
            alreadyRegistered = True
            return render_template('main_page.html', alreadyRegistered=alreadyRegistered)

    # If reaches here, then author either doesn't exist or doesn't have a book by the name. Check for nonexistence first
    if (aId is None):
        # New author, need to add to the Authors table

        # Calculate a new author ID and add to Authors database
        aId = add_new_author(bookauthorfirst.capitalize(), bookauthorsecond.capitalize())

    # Author has been added to database if not previously existing. Book can now be registered

    # Calculate a new book ID
    max_id = get_new_book_id()

    # Insert -- attribute order is : id, name, author, genre, rating
    newbook = BookClass(max_id, bookname, aId, bookgenre.capitalize())
    newbook.save_to_db()

    if (bookrating is not None and bookrating != ''):
        print("bookrating is not None!")
        print(bookrating)
        rId = get_new_rating_id()

        tempuserId = 1
        newrating = RatingClass(rId, tempuserId, max_id, bookrating)
        newrating.save_to_db()

    conn.commit()
    conn.close()

    success = True
    return render_template('main_page.html', success=success)

# Generate Report Form
@app.route('/query', methods=['POST'])
def query_database():
    genre_input = request.form['genre_input']
    author_input = request.form['author_input']
    rating_input = request.form['rating_input']

    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # Execute an SQL query using the user's input

    query_str = 'SELECT * FROM Books b'
    firstFilter = True
    if (genre_input != ''):
        # add functionality for list of genres
        firstFilter = False
        query_str += ' WHERE LOWER(b.genre) == "' + genre_input.lower() + '"'

    if (author_input != ''):
        # add functionality for list of authors
        author_names = author_input.split(' ');
        aId = 0;
        cursor.execute('SELECT authorId FROM Authors a WHERE a.firstname = ? '
                       'AND a.lastname = ?',
                       (author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize()))
        results = cursor.fetchone()
        aId = results[0]

        if firstFilter:
            query_str += ' WHERE'
        else:
            query_str += ' AND'
        query_str += ' b.authorId == ' + str(aId)

    if (rating_input != ''):
        # add calculation of rating for each book
        if firstFilter:
            query_str += ' WHERE'
        else:
            query_str += ' AND'
        query_str += ' b.rating == ' + rating_input

    query_str += ';'
    cursor.execute(query_str)
    result = cursor.fetchall()
    conn.close()

    # Process the result and return it to the user
    #if (len(result) == 0):
    #    return render_template('empty_results.html')

    return render_template('results.html', data=result)

@app.route('/edit', methods=['GET', 'POST'])
def edit_book_entries():
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        selected_entry_id = request.form.get('selected_entry_id')
        return redirect(url_for('edit_bookdatabase', entry_id=selected_entry_id))

    # Fetch all entries for display
    cursor.execute('SELECT Books.bookId, Books.name, Authors.firstname, Authors.lastname, Books.genre FROM Books LEFT JOIN Authors ON Books.authorId = Authors.authorId')
    entries = cursor.fetchall()

    cursor.close()
    conn.close()

    #author_names = [get_full_author_name(entry[2]) for entry in entries]
    return render_template('editBookEntries.html', entries=entries)
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_bookdatabase(entry_id):
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Handle form submission for edits
        new_name = request.form['name']
        new_author = request.form['author']
        new_genre = request.form['genre']

        author_names = new_author.split(' ')

        replaceBook = BookClass.get_book_with_id(entry_id)
        replaceBook.update_book_data(new_name, author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize(), new_genre)

        return redirect(url_for('edit_book_entries'))

    # Fetch existing data for pre-population
    cursor.execute('SELECT Books.bookId, Books.name, Authors.firstname, Authors.lastname, Books.genre '
                   'FROM Books LEFT JOIN Authors ON Books.authorId = Authors.authorId WHERE Books.bookId = ?', (entry_id,))
    entry = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editBooks.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_book_entry(entry_id):
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    selected_entry_id = request.form.get('selected_entry_id')

    cursor.execute("DELETE FROM Books WHERE bookId = ?", (selected_entry_id,))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('edit_book_entries'))

if __name__ == '__main__':
    # reset_database()
    #app.run(host='127.0.0.1', debug=True)
    app.run()