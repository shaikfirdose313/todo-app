from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/")
def index():
    db = get_db()
    todos = db.execute("SELECT * FROM todos").fetchall()
    return render_template("index.html", todos=todos)
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    db = get_db()
    db.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (task, 0))
    db.commit()
    return redirect("/")
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id=?", (id,))
    db.commit()
    return redirect("/")
@app.route("/toggle/<int:id>")
def toggle(id):
    db = get_db()
    todo = db.execute("SELECT completed FROM todos WHERE id=?", (id,)).fetchone()
    new_value = 0 if todo["completed"] == 1 else 1
    db.execute("UPDATE todos SET completed=? WHERE id=?", (new_value, id))
    db.commit()
    return redirect("/")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = get_db()
    if request.method == "POST":
        task = request.form["task"]
        db.execute("UPDATE todos SET task=? WHERE id=?", (task, id))
        db.commit()
        return redirect("/")
    todo = db.execute("SELECT * FROM todos WHERE id=?", (id,)).fetchone()
    return render_template("edit.html", todo=todo)
if __name__ == "__main__":
    app.run()