import sqlite3
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, make_response
from flask import Flask, render_template, request, redirect, url_for, flash

import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
db_name = 'users.db'


@app.route('/')
def index():
    return render_template('index.html')


# Initialize the database table
def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL,
                 points INTEGER)''')
    conn.commit()
    conn.close()


init_db()


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the email already exists in the database
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user:
            error = 'This email address is already registered. Please choose another one.'
            return render_template('signup.html', error=error)
        elif password != confirm_password:
            error = 'The passwords you entered do not match. Please try again.'
            return render_template('signup.html', error=error)
        else:
            # Add the user to the database
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password, points) VALUES (?, ?, ?, ?)", (username, email, password, 0))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email and password match a user in the database
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['progress'] = user[4]
            return render_template('game.html')
        else:
            error = 'Incorrect email or password. Please try again.'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')


db1_name = 'admin.db'


# Signup route
@app.route('/clear_data', methods=['GET', 'POST'])
def clear_data():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''DELETE FROM users''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('''DELETE FROM admins''')
    conn.commit()
    conn.close()
    return "Data Deleted Succesfully"
# Initialize the database table
def init1_db():
    conn = sqlite3.connect(db1_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL,
                 secret_key INTEGER)''')
    conn.commit()
    conn.close()


init1_db()


# Signup route
@app.route('/asignup', methods=['GET', 'POST'])
def signup1():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        secret_key = request.form['secret_key']
        
        # Check if the email already exists in the database
        conn = sqlite3.connect(db1_name)
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user:
            error = 'This email address is already registered. Please choose another one.'
            return render_template('asignup.html', error=error)
        elif password != confirm_password or secret_key != 123:
            error = 'The passwords you entered do not match. Please try again.'
            return render_template('asignup.html', error=error)
        else:
            # Add the user to the database
            conn = sqlite3.connect(db1_name)
            c = conn.cursor()
            c.execute("INSERT INTO admins (username, email, password, secret_key) VALUES (?, ?, ?, ?)", (username, email, password, secret_key))
            conn.commit()
            conn.close()
            return redirect(url_for('alogin'))
    else:
        return render_template('asignup.html')


# Login route
@app.route('/alogin', methods=['GET', 'POST'])
def alogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'shaikfouziya.20.cse@anits.edu.in' and password == 'fouzi':
            session['user_id'] = 'admin'
            session['progress'] = 0
            return render_template('agame.html')
        else:
            error = 'Incorrect email or password. Please try again.'
            return render_template('alogin.html', error=error)
    else:
        return render_template('alogin.html')
    
# Route to display all users
@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY points DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('users.html', rows=rows)

# Logout route
@app.route('/logout')
def logout():
    # Save the user's progress before logging them out
    user_id = session.get('user_id')
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/game.html')
def game():
    return render_template('game.html')

@app.route('/agame.html')
def agame():
    return render_template('agame.html')

@app.route('/selection')
def selection():
    return render_template('selection.html')
# Resume route
@app.route('/resume')
def resume():
    return render_template('game.html')

@app.route('/clues')
def clues():
    return render_template('clues.html')

@app.route('/avisual')
def avisual():
    return render_template('avisual.html')

@app.route('/visual.html')
def visualize():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get user data from database
    c.execute('SELECT * FROM users ORDER BY points DESC')
    users = c.fetchall()

    conn.close()

    # Pass user data to visual.html template
    return render_template('visual.html', users=users)

@app.route('/clues/<int:clue_num>.html')
def clue(clue_num):
    return render_template('clues/{}.html'.format(clue_num))

@app.route('/treasure.html')
def treasure():
    return render_template('treasure.html')

@app.route('/clues/game.html')
def game1():
    return render_template('clues/game.html')


@app.route('/check-user')
def check_user():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'not logged in'})
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE username=?", (username,))
    progress = c.fetchone()
    if progress:
        return jsonify({'progress': progress[0]})
    else:
        return jsonify({'error': 'user not found'})

@app.route('/update_points', methods=['POST'])
def update_points():
    user_id = session['user_id']
    points = request.json['points']
    
    # Update the user's points in the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET points=? WHERE id=?', (points, user_id))
    conn.commit()
    conn.close()
    
    return 'OK'

@app.route('/leaderboard_data')
def leaderboard_data():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, points FROM users ORDER BY points DESC')
    data = [{'username': row[0], 'points': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True,port=8000)
