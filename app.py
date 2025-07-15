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

from flask import Flask, render_template
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
db.__init__(app)

# initialize the database with the Flask app
class Status(Enum):
    COMPLETED = 'Completed'
    INCOMPLETED = 'Incompleted'


class MyTask(db.Model):
    id= db.Column(db.Integer, primary_key = True )
    content= db.Column(db.String(100), nullable= False)
    status= db.Column(db.Enum (Status, name='task_status'), default= Status.INCOMPLETED.value)
    data_created= db.Column(db.DateTime, default= datetime.now)

    def __repr__(self):
        return f"Task {self.id}"
    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
