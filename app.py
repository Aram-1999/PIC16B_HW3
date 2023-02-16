from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')

def get_message_db():
    """
    This function checks whether message_db database exists or not.
    If it exists, it returns the database, otherwise it creates a 
    database with a table of 2 text columns and an integer column, 
    and return the connection to it.  
    """
    g.message_db = sqlite3.connect("message_db.sqlite")
    cur = g.message_db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id integer,
        handle text,
        message text)
    """)
    return g.message_db

def insert_message(request):
    message = request.form["message"]
    name = request.form["name"]

    get_message_db()
    db = g.message_db
    cur = db.cursor()

    cur.execute("SELECT COUNT(id) as count FROM messages")
    id = int(cur.fetchall()[0][0]) + 1

    cur.execute("""
    INSERT INTO messages (id, handle, message)
    VALUES (?, ?, ?);
    """,(str(id), name, message))

    db.commit()
    db.close()
    
@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    #return render_template('submit.html')
    if request.method == 'GET':
        return render_template('submit.html',message="")
    else:
        insert_message(request)
        return render_template('submit.html',
        message="Thank you for creating a message")

def random_messages(n):
    db = get_message_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT ?;",str(n))

    records = cur.fetchall()
    db.close()
    return records

@app.route('/view')
def view():
    messages = random_messages(8)
    return render_template('view.html', messages=messages)
