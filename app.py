import sqlite3
from flask import Flask, render_template, request, g, redirect
app = Flask(__name__)

DATABASE = 'brady_demo.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def sign_up():
    db = get_db()
    db.execute("INSERT INTO friends (name) VALUES ('{}')".format(request.form['name']))
    db.commit()
    return redirect('/friends/')

@app.route('/friends/')
def friends_list():
    db = get_db()
    res = db.execute("select * from friends")
    friends = res.fetchall()
    friends = [friend[0] for friend in friends]
    return render_template('friends.html', friends=friends)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        # Create table
        db.execute('''CREATE TABLE friends
                      (name text)''')
        db.commit()


if __name__ == '__main__':
    app.run(debug=True)
