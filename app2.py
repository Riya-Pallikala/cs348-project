import datetime

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    success = False
    return render_template('main_page.html', success=success)

# Authors Table
class AuthorClass:
    def __init__(self, authorId, firstname, lastname):
        self.authorId = authorId
        self.firstname = firstname
        self.lastname = lastname

    # ORM get id given name
    #def get_id_from_name(self, fname, last):

    # ORM insert
    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert row with passed values
        cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?)',
                       (self.authorId, self.firstname, self.lastname))

        conn.commit()
        cursor.close()
        conn.close()

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

# Books Table
class BookClass:
    def __init__(self, bookId, name, authorId, genre, rating=None):
        self.bookId = bookId
        self.name = name
        self.authorId = authorId
        self.genre = genre
        self.rating = rating

    # ORM select matching ID
    def get_book_with_id(bookid):
        conn = sqlite3.connect('databases/test_db1.db')
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

    # ORM update book's author
    def update_book_data(self, name, authorfirstname, authorlastname, genre):

        self.name = name
        self.genre = genre

        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE Books SET name = ?, genre = ? WHERE bookId  = ?', (self.name, self.genre, self.bookId))

        conn.commit()
        cursor.close()
        conn.close()



    # ORM insert
    def save_to_db(self):
        conn = sqlite3.connect('databases/test_db1.db')
        cursor = conn.cursor()

        # Insert passed data
        cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);',
                       (self.bookId, self.name, self.authorId, self.genre))

        conn.commit()
        cursor.close()
        conn.close()

def get_new_book_id():
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    max_id = 0
    cursor.execute('SELECT max(bookId) from Books;')
    result = cursor.fetchone()

    if (result is None or result[0] is None):
        # empty booklist, this will be the first
        max_id = 1
    else:
        # increment largest ID by 1, will be unique ID
        max_id = result[0] + 1

    conn.commit()
    cursor.close()
    conn.close()
    return max_id

# Reset Database to default starting data
# @app.route('/', methods=['POST', 'GET'])
def reset_database():
    # Change to stored procedure?
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # drop tables to reset
    cursor.execute('DROP TABLE IF EXISTS Books;')
    cursor.execute('DROP TABLE IF EXISTS Authors;')

    # Create tables Authors(authorId, firstname, lastname)
    cursor.execute('CREATE TABLE IF NOT EXISTS Authors '
                   '(authorId INTEGER PRIMARY KEY, '
                   'firstname TEXT, '
                   'lastname TEXT);')

    # use ORM to insert each author instance

    newAuthor1 = AuthorClass(1, "Leigh", "Bardugo")
    newAuthor1.save_to_db()

    newAuthor2 = AuthorClass(2, "Neil", "Gaiman")
    newAuthor2.save_to_db()

    newAuthor3 = AuthorClass(3, "William", "Shakespeare")
    newAuthor3.save_to_db()

    newAuthor4 = AuthorClass(4, "Agatha", "Christie")
    newAuthor4.save_to_db()

    newAuthor5 = AuthorClass(5, "Madeline", "Miller")
    newAuthor5.save_to_db()

    newAuthor6 = AuthorClass(6, "Robert", "Frost")
    newAuthor6.save_to_db()

    newAuthor7 = AuthorClass(7, "Stephen", "King")
    newAuthor7.save_to_db()

    newAuthor8 = AuthorClass(8, "Michelle", "Obama")
    newAuthor8.save_to_db()

    newAuthor9 = AuthorClass(9, "Kevin", "Kwan")
    newAuthor9.save_to_db()

    newAuthor10 = AuthorClass(10, "Robin", "Kimmerer")
    newAuthor10.save_to_db()

    # Create Books(bookId, name, authorId, genre, length_in_pages)
    cursor.execute('CREATE TABLE IF NOT EXISTS Books '
                   '(bookId INTEGER PRIMARY KEY, '
                   'name TEXT, '
                   'authorId INTEGER, '
                   'genre TEXT, '
                   'FOREIGN KEY(authorId) REFERENCES Authors(authorId));')

    # use ORM to insert each author instance

    newBook1 = BookClass(1, "Six of Crows", 1, "Fantasy")
    newBook1.save_to_db()

    newBook1 = BookClass(2, "Coraline", 2, "Fantasy")
    newBook1.save_to_db()

    newBook1 = BookClass(3, "Romeo and Juliet", 3, "Play")
    newBook1.save_to_db()

    newBook1 = BookClass(4, "Murder on the Orient Express", 4, "Mystery")
    newBook1.save_to_db()

    newBook1 = BookClass(5, "The Song of Achilles", 5, "Historical Fiction")
    newBook1.save_to_db()

    newBook1 = BookClass(6, "The Road Not Taken", 6, "Poetry")
    newBook1.save_to_db()

    newBook1 = BookClass(7, "It", 7, "Horror")
    newBook1.save_to_db()

    newBook1 = BookClass(8, "Becoming", 8, "Autobiography")
    newBook1.save_to_db()

    newBook1 = BookClass(9, "Crazy Rich Asians", 9, "Romance")
    newBook1.save_to_db()

    newBook1 = BookClass(10, "Braiding Sweetgrass", 10, "Contemporary")
    newBook1.save_to_db()

    create_indexes()

    conn.commit()
    cursor.close()
    conn.close()

    return

def create_indexes():
    conn = sqlite3.connect('databases/test_db1.db')
    cursor = conn.cursor()

    # create index on author names
    cursor.execute('CREATE INDEX authorsNames ON Authors (firstname, lastname)');

    # create index on book ratings

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['POST', 'GET'])
def update_database():
    success = False
    alreadyRegistered = False

    bookname = request.form['newbook_input']
    bookauthorfirst = request.form['newauthorfirst_input']
    bookauthorsecond = request.form['newauthorsecond_input']
    bookgenre = request.form['newgenre_input']


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

    # Insert -- attribute order is : id, name, genre, author, length
    newbook = BookClass(max_id, bookname.capitalize(), aId, bookgenre.capitalize())
    newbook.save_to_db()

    #cursor.execute('INSERT INTO Books (bookId, name, authorId, genre)  VALUES (?, ?, ?, ?);', (max_id, bookname, aId, bookgenre.capitalize()))
    conn.commit()
    conn.close()

    success = True
    return render_template('main_page.html', success=success)

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
    #cursor.execute('SELECT * FROM Books;')
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
    app.run(host='127.0.0.1', debug=True)
  #  app.run()