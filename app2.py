import datetime

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_session import Session

from markupsafe import Markup

from ORM_Classes import AuthorClass, BookClass, UserClass, RatingClass

from helper_author import *
from helper_book import *
from helper_rating import *
from helper_user import *
from helper_database import *

app = Flask(__name__)
#app.secret_key = '348riyakey'
app.config['SECRET_KEY'] = '348riyakey18'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_USE_SIGNER"] = True

Session(app)

# Handle only html page rendering and processing in this file
# ORM class logic abstracted to ORM_Classes.py
# Helper functions that are not Class defs abstracted to respectively named helper files
# Helper functions for general database setup abstracted to helper_database.py

# Home Page
@app.route('/')
def home():
    success = False
    if 'user' in session:
        user = session['user']
        return render_template('main_page.html', title=f'Hello, {user}! Welcome to the Book Recommender!', success=success)
    else:
        return render_template('main_page.html', title='Hello, Welcome to the Book Recommender!', success=success)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("trying to signup")
        # Validate credentials
        currUserId = get_userid_from_username(username)
        if currUserId is not None:
            print("taken username")
            taken_user_message = Markup('This username is already taken! Please <a href="{}">login</a> to that account '
                                   'or choose a different username'.format(url_for('login')))
            return render_template('signup.html', taken_user_message=taken_user_message)

        else:
            print("new username")
            # add new User, create session, then redirect to home page
            add_new_user(username, password)
            session['user'] = username
            return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate credentials
        currUserId = get_userid_from_username(username)
        if currUserId is not None:
            pwdIsCorrect = validate_password(currUserId, password)

            if pwdIsCorrect:
                session['user'] = username
                return redirect(url_for('home'))
            else:
                # wrong password
                error_message = 'Incorrect password for this username!'
                return render_template('login.html', error_message=error_message)

        else:
            # not yet registered - redirect to sign up
            signup_message = Markup('Username not found! Register here: <a href="{}">Sign Up!</a>'.format(url_for('signup')))
            return render_template('login.html', signup_message=signup_message)

    return render_template('login.html')

@app.route('/guest_login')
def guest_login():
    # guest, not logged in
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove 'user' from the session
    return redirect(url_for('home'))


# Add Book Form
@app.route('/', methods=['POST', 'GET'])
def update_database():
    success = False
    alreadyRegistered = False

    bookname = request.form['newbook_input'].strip()
    bookauthorfirst = request.form['newauthorfirst_input'].strip()
    bookauthorsecond = request.form['newauthorsecond_input'].strip()
    bookgenre = request.form['newgenre_input'].strip()
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

    # Insert -- attribute order is : id, name, author, genre, rating (optional, default None)
    newbook = BookClass(max_id, bookname, aId, bookgenre.capitalize())
    newbook.save_to_db()

    if (bookrating is not None and bookrating != ''):
        # print("bookrating is not None!")
        # print(bookrating)
        rId = get_new_rating_id()

        currUserId = get_userid_from_username(session['user'])
        newrating = RatingClass(rId, currUserId, max_id, bookrating)
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
    match_mode = request.form['match_option_input']

    operator = ""
    if match_mode == 'all':
        operator = "AND"
    else:
        operator = "OR"

    match_string = " " + operator + " ("

    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    unfound_list = []

    # Execute an SQL query using the user's input

    query_str = 'SELECT b.bookId, b.name, firstname, lastname, b.genre, b.ave_rating FROM Books b JOIN Authors ON Authors.authorId = b.authorId'
    firstFilter = True
    if (genre_input != ''):
        firstFilter = False
        genre_input_list = genre_input.split(",")

        firstgenre = True
        for genre in genre_input_list:
            # add iteration of list of genres
            if firstgenre:
                query_str += ' WHERE ( LOWER(b.genre) = "' + genre.strip().lower() + '"'
                firstgenre = False
            else:
                query_str += ' OR LOWER(b.genre) = "' + genre.strip().lower() + '"'

        query_str += ')'

    if (author_input != ''):
        # add functionality for list of authors

        author_input_list = author_input.split(",")

        firstauthor = True
        authorExists = False # only set to true when we know at least one author has been added to the list

        for author in author_input_list:
            # add iteration of list of authors

            # get id from name of current author
            author_names = author.strip().split(' ')

            aId = 0
            aId = get_authorid_from_name(author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize())

            if (aId is None):
                # the entered author does not exist in the database
                # print("invalid author names.")
                unfound_list.append((author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize()))
                pass
            else:
                authorExists = True
                # add to query to search for current author
                if firstauthor:
                    if firstFilter:
                        query_str += ' WHERE ('
                    else:
                        query_str += match_string
                    query_str += ' b.authorId == ' + str(aId)

                    firstauthor = False
                else:
                    query_str += ' OR b.authorId = ' + str(aId)

        if authorExists:
            query_str += ')'


    if (rating_input != ''):
        # add calculation of rating for each book
        if firstFilter:
            query_str += ' WHERE ('
        else:
            query_str += match_string
        query_str += ' b.ave_rating >= ' + rating_input + ' OR b.ave_rating IS NULL)'

    query_str += ' ORDER BY b.ave_rating DESC, lastname, firstname, genre;'
    print("query is :" + query_str)
    cursor.execute(query_str)
    result = cursor.fetchall()
    conn.close()

    # Process the result and return it to the user
    if (len(result) == 0):
        return render_template('empty_results.html')

    return render_template('results.html', data=result, unfound_authors=unfound_list)

@app.route('/edit', methods=['GET', 'POST'])
def edit_book_entries():
    # Connect to the database
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        selected_entry_id = request.form.get('selected_entry_id')
        return redirect(url_for('edit_bookdatabase', entry_id=selected_entry_id))

    # Fetch all entries for display
    cursor.execute('SELECT Books.bookId, Books.name, Authors.firstname, Authors.lastname, Books.genre, Books.ave_rating, Ratings.rating '
                   'FROM Books LEFT JOIN Authors '
                   'ON Books.authorId = Authors.authorId '
                   'LEFT JOIN Ratings '
                   'ON Ratings.bookId = Books.bookId AND Ratings.userId = ?',
                   (get_userid_from_username(session['user']),))
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
        # new_name = request.form['name']
        # new_author = request.form['author']
        new_genre = request.form['genre']
        new_rating = request.form['rating']

        # author_names = new_author.split(' ')

        # find book entry in Books table
        replaceBook = BookClass.get_book_with_id(entry_id)

        if (replaceBook.ave_rating != new_rating):
            # need to update the rating the user submitted for this book
            uId = get_userid_from_username(session['user'])
            replaceRating = RatingClass.get_ratingid_given_user_and_book(uId, entry_id)

            if replaceRating is None:
                # no current rating for that user, make a new one
                replaceRating = RatingClass(get_new_rating_id(), uId, entry_id, new_rating)
                replaceRating.save_to_db()
            else:
                # old rating exists, update value
                replaceRating.update_rating_data(new_rating)

        #replaceBook.update_book_data(new_name, author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize(), new_genre)
        # updated to only allow editing of genre and rating
        replaceBook.update_book_data(new_genre)

        return redirect(url_for('edit_book_entries'))

    # Fetch existing data for pre-population
    """cursor.execute('SELECT Books.bookId, Books.name, Authors.firstname, Authors.lastname, Books.genre '
                   'FROM Books LEFT JOIN Authors ON Books.authorId = Authors.authorId WHERE Books.bookId = ?', (entry_id,))"""
    cursor.execute(
        'SELECT Books.bookId, Books.name, Authors.firstname, Authors.lastname, Books.genre, Ratings.rating '
        'FROM Books LEFT JOIN Authors '
        'ON Books.authorId = Authors.authorId '
        'LEFT JOIN Ratings '
        'ON Ratings.bookId = Books.bookId AND Ratings.userId = ?'
        'WHERE Books.bookId = ?',
        (get_userid_from_username(session['user']), entry_id))
    entry = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editBooks.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_book_entry(entry_id):
    # Connect to the database

    selected_entry_id = request.form.get('selected_entry_id')

    delete_book_with_id(selected_entry_id)

    return redirect(url_for('edit_book_entries'))

@app.route('/deleterating/<int:entry_id>', methods=['POST'])
def delete_book_rating(entry_id):

    selected_entry_id = request.form.get('selected_entry_id')
    delete_rating_with_user_and_book(get_userid_from_username(session['user']), selected_entry_id)

    return redirect(url_for('edit_book_entries'))

if __name__ == '__main__':
    # reset_database()
    #app.run(host='127.0.0.1', debug=True)
    app.run()