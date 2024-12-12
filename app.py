from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "AprioriKS"

DATABASE = "database.db"


def session():
    connection = sqlite3.connect("database.db")
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


@app.get("/add/")
def add_finance():
    return render_template("add.html")


@app.post("/add/")
def add_finance_post():
    cash = request.form["cash"]
    content = request.form["content"]
    connection = session()
    connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (cash, content))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))



@app.get("/<int:post_id>/edit")
def get_edit(post_id):
    connection = session()
    post = connection.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    connection.close()
    return render_template("edit.html", post=post)


@app.post("/<int:post_id>/edit")
def post_edit(post_id):
    connection = session()
    cash = request.form["cash"]
    content = request.form["content"]
    connection.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (cash, content, post_id))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.post("/delete")
def delete(post_id):
    connection = session()
    connection.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=808080080808080808)
