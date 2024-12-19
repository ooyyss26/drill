import pytest
from flask import jsonify
from app import create_app, db, Account

@pytest.fixture
def app():
    # Create the app instance with the database URI pointing to your existing database
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:root@localhost/access_control',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

 # Set up a database transaction before each test
    with app.app_context():
        db.create_all()
        db.session.begin()  # Begin a transaction

    yield app  # This will run the test

    # After test execution, rollback all changes to the database
    with app.app_context():
        db.session.rollback()  # Rollback any changes
        db.session.remove()  # Remove the session to clean up

@pytest.fixture
def client(app):
    # Return a test client for making HTTP requests
    return app.test_client()