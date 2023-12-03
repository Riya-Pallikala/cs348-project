import datetime

from flask import Flask, render_template, request
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


# Books Table
class BookClass:
    def __init__(self, bookId, name, authorId, genre):
        self.bookId = bookId
        self.name = name
        self.authorId = authorId
        self.genre = genre

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


    conn.commit()
    cursor.close()
    conn.close()

    return

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
    aId = 0
    cursor.execute('SELECT authorId FROM Authors a WHERE LOWER(a.firstname) = LOWER(?) AND LOWER(a.lastname) = LOWER(?)',
                   (bookauthorfirst.capitalize(), bookauthorsecond.capitalize()))
    result = cursor.fetchone()

    if (result is not None):
        aId = result[0]
    else:
        aId = None

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

        # Calculate a new author ID
        cursor.execute('SELECT max(authorId) from Authors;')
        result = cursor.fetchone()
        if (result[0] is None):
            aId = 1
        else:
            aId = result[0] + 1


        # Add new author to Authors table
        newauthor = AuthorClass(aId, bookauthorfirst.capitalize(), bookauthorsecond.capitalize())
        newauthor.save_to_db()

        #cursor.execute('INSERT INTO Authors (authorId, firstname, lastname) VALUES (?, ?, ?);', (aId, bookauthorfirst.capitalize(), bookauthorsecond.capitalize()))


    # Author has been added to database if not previously existing. Book can now be registered

    # Calculate a new book ID
    max_id = 0
    cursor.execute('SELECT max(bookId) from Books;')
    result = cursor.fetchone()

    if (result is None or result[0] is None):
        # empty booklist, this will be the first
        max_id = 1
    else:
        # increment largest ID by 1, will be unique ID
        max_id = result[0] + 1


    # Insert -- attribute order is : id, name, genre, author, length
    newbook = BookClass(max_id, bookname, aId, bookgenre.capitalize())
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
        firstFilter = False
        query_str += ' WHERE LOWER(b.genre) == "' + genre_input.lower() + '"'

    if (author_input != ''):
        author_names = author_input.split(' ');
        aId = 0;
        cursor.execute('SELECT authorId FROM Authors a WHERE LOWER(a.firstname) = LOWER(?) '
                       'AND LOWER(a.lastname) = LOWER(?)',
                       (author_names[0].capitalize(), author_names[len(author_names) - 1].capitalize()))
        results = cursor.fetchone()
        aId = results[0]

        if firstFilter:
            query_str += ' WHERE'
        else:
            query_str += ' AND'
        query_str += ' b.authorId == ' + str(aId)

    if (rating_input != ''):
        # stored procedure to calculate rating for each book
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

if __name__ == '__main__':
    reset_database()
    app.run(debug=True)