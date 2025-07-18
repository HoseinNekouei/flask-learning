"""
This module sets up a simple Flask web application with SQLAlchemy integration and SCSS support.
Classes:
    Status (Enum): Enumeration for task status with values 'Completed' and 'Incompleted'.
    MyTask (db.Model): SQLAlchemy model representing a task with fields for id, content, status, and creation date.
Functions:
    index(): Flask route for the root URL ('/'), renders the 'index.html' template.
App Initialization:
    - Configures Flask app and SQLAlchemy with an SQLite database.
    - Initializes SCSS support for the app.
    - Creates all database tables if run as the main module.
    - Runs the Flask development server in debug mode.
"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime
from enum import Enum

# create the app
app = Flask(__name__)
Scss(app)
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]= False
db.__init__(app)



task_status = ['Completed', 'Incompleted']

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=task_status[1])
    data_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()


# route to webpages
# Homepage
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        content = request.form['content']
        new_task= MyTask(content=content)

        try:
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            print(f'ERROR: {e}')

        return redirect('/')

    else:
        # see all the current tasks
        add_task= MyTask.query.order_by(MyTask.data_created.asc()).all()
        return render_template('index.html', tasks=add_task)


#Delete an Item
@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id: int):
    delete_task= MyTask.query.get_or_404(task_id)

    try:
        db.session.delete(delete_task)
        db.session.commit()

    except Exception as e:
        print(f'Error: {e}')

    return redirect('/')


# update an Item
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id: int):
    
    update_task= MyTask.query.get_or_404(task_id)
    
    if request.method == 'POST':
        update_task.content= request.form['content']

        try:
            db.session.commit()

        except Exception as e:
            print(f'Error: {e}')
        
        return redirect('/')
    
    else:
        return render_template('update.html', task= update_task)


if __name__ == '__main__':



    app.run(debug=True)