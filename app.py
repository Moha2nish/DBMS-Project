from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder='templates')

conn = sqlite3.connect('tasks.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    task_name TEXT NOT NULL,
    task_description TEXT,
    due_date DATE,
    status TEXT,
    priority TEXT
)''')
conn.commit()
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    c.execute("INSERT INTO tasks (task_name, task_description, due_date, priority) VALUES (?, ?, ?, ?)", (task_name, task_description, due_date, priority))
    conn.commit()
    conn.close()
    return redirect('/')




@app.route('/update/<int:id>', methods=['GET'])
def show_update_form(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()
    return render_template('update.html', task=task)

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    c.execute("UPDATE tasks SET task_name=?, task_description=?, due_date=?, priority=? WHERE id=?", (task_name, task_description, due_date, priority, id))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/delete/<int:id>', methods=['GET'])
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
