from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/query', methods=['POST'])
def query_database():
    user_input = request.form['user_input']

    # Connect to the database
    conn = sqlite3.connect('databases/test_db.db')
    cursor = conn.cursor()

    # Execute an SQL query using the user's input
    # cursor.execute('SELECT * FROM your_table WHERE column_name = ?', (user_input))

    # Create Authors(authorId, firstname, lastname, birth_year, death_year)
    cursor.execute('CREATE TABLE IF NOT EXISTS Authors '
                   '(authorId INTEGER PRIMARY KEY, '
                   'firstname TEXT, '
                   'lastname TEXT, '
                   'birth_year DATETIME, '
                   'death_year DATETIME);')

    # Create Books(bookId, name, authorId, genre, length_in_pages)
    cursor.execute('CREATE TABLE IF NOT EXISTS Books (bookId INTEGER PRIMARY KEY, name TEXT, authorId INTEGER, FOREIGN KEY (authorId) REFERENCES Authors(authorId));')

    cursor.execute('SELECT * FROM Books;')
    result = cursor.fetchall()
    conn.close()

    # Process the result and return it to the user
    if (len(result) == 0):
        return render_template('empty_results.html')

    return render_template('results.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)