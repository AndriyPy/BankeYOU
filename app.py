from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "AprioriKS"

DATABASE = "database.db"


def session():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with session() as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cash INTEGER NOT NULL,
            title TEXT NOT NULL
        )
        """)
        connection.commit()
        connection.close()


@app.get("/")
def index():
    connection = session()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=808080080808080808)
