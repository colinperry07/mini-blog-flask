from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('blog.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

#access data once on startup
with get_db_connection() as connection:
    connection.execute('''CREATE TABLE IF NOT EXISTS posts (title TEXT, content TEXT) ''')
    connection.commit()


@app.route("/")
def home():
    connection = get_db_connection()
    rows = connection.execute("SELECT title, content FROM posts").fetchall()
    posts = [{'title': row[0], 'content': row[1]} for row in rows]
    return render_template("index.html", posts=posts)

@app.route("/new", methods=["GET", "POST"])
def new_post():
    
    connection = get_db_connection()
    
    if request.method == "POST":
        
        title = request.form['title']
        content = request.form['content']
        
        connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        connection.commit()
        connection.close()
        
        return redirect('/')
    
    return render_template("new_post.html")


if __name__ == "__main__":
    app.run(debug=True)