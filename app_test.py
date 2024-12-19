import pytest
from flask import jsonify
from app import create_app, db, User

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

# Test for home route
def test_home(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Users Access Control'

def test_get_users(client):
    # Obtain a valid token by logging in
    login_response = client.post('/login', json={'username': 'admin', 'password': 'admin'})
    
    # Ensure login was successful
    assert login_response.status_code == 200
    
    # Get the token from the response
    token = login_response.get_json()['access_token']  # Access the correct key for the token
    
    # Make authenticated request to the /users route
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/users', headers=headers)
    
    # Ensure the response is successful
    assert response.status_code == 200

def test_get_users_access_denied(client):
    # Send a GET request to retrieve the list of users without a valid token
    response = client.get('/users')

    # Assert that the status code is 401 (Unauthorized)
    assert response.status_code == 401

def test_create_user(client):
    # Data for creating a new user
    user_data = {
        'user_id': 4,
        'role_code': 'admin',  # Assume this role exists in the roles table
        'user_frst_name': 'John',
        'user_last_name': 'Doe',
        'user_login': 'johndoe',
        'password': 'password123',
        'other_details': 'Some details about the user',
        'Roles_role_code': 1  # Assuming this maps to a valid role in the roles table
    }

    # Make a POST request to create a user
    response = client.post('/users', json=user_data)

    # Assert that the user is created successfully (status code 201)
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_update_user(client):
    # Data to update the user
    updated_data = {
        'user_frst_name': 'Johnathan', 
        'user_last_name': 'Doe',
        'user_login': 'johnathandoe',
        'password': 'newpassword123',
        'other_details': 'Updated details about Johnathan'
    }

    # Send a PUT request to update the user with user_id 1
    response = client.put('/users/4', json=updated_data)

    # Assert that the status code is 200 (success)
    assert response.status_code == 200
    assert b'User updated successfully' in response.data

# Test for deleting an account
def test_delete_user(client):
    response = client.delete('/users/4')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'User and related access rights deleted successfully'