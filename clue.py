from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db_name = 'users.db'

# function to create table in database
def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 progress INTEGER NOT NULL DEFAULT 0,
                 start_time DATETIME)''')
    conn.commit()
    conn.close()

# function to get user's progress from the database
def get_user_progress(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT progress FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return 0

# function to update user's progress in the database
def update_user_progress(username, progress):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("UPDATE users SET progress=? WHERE username=?", (progress, username))
    conn.commit()
    conn.close()

# function to update user's start time in the database
def update_user_start_time(username, start_time):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("UPDATE users SET start_time=? WHERE username=?", (start_time, username))
    conn.commit()
    conn.close()

# function to get user's start time from the database
def get_user_start_time(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT start_time FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result is not None:
        return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
    else:
        return datetime.now()

# route for the first clue
@app.route('/clue1')
def clue1():
    # get the user's progress from the session
    progress = session.get('progress', 0)
    # increment the user's progress by 1 for completing this clue
    progress += 1
    # update the user's progress in the session and the database
    session['progress'] = progress
    update_user_progress(session['username'], progress)
    # update the user's start time in the session and the database
    start_time = session.get('start_time', datetime.now())
    session['start_time'] = start_time
    update_user_start_time(session['username'], start_time.strftime('%Y-%m-%d %H:%M:%S.%f'))
    # render the template for the first clue
    return render_template('clue1.html', progress=progress)

# main route for the game
@app.route('/game')
def game():
    # check if the user is logged in
    if 'username' in session:
        # get the user's progress from the database
        progress = get_user_progress(session['username'])
        # render the template for the game with the user's progress
        return render_template('game.html', progress=progress)
    else:
        # redirect the user to the login page if they are not logged in
        return redirect('/login')

# login route
# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if the user is already logged in
    if 'username' in session:
        return redirect('/game')
    # if the request method is POST, attempt to log in the user
    if request.method == 'POST':
        # get the login form data
        username = request.form['username']
        password = request.form['password']
        # connect to the database and check if the user exists
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()
        # if the user exists, log them in
        if result is not None:
            session['username'] = username
            # redirect the user to the game
            return redirect('/game')
        else:
            # if the user does not exist, show an error message
            error = 'Invalid username or password.'
            return render_template('login.html', error=error)
    # if the request method is GET, show the login form
    else:
        return render_template('login.html')

# logout route
@app.route('/logout')
def logout():
    # clear the user's session and redirect them to the login page
    session.clear()
    return redirect('/login')

# run the app
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
    
