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

# def test_get_users(client):
#     # Obtain a valid token by logging in
#     login_response = client.post('/login', json={'username': 'admin', 'password': 'admin'})
    
#     # Ensure login was successful
#     assert login_response.status_code == 200, f"Login failed with status code {login_response.status_code}"
    
#     # Get the token from the response
#     login_data = login_response.get_json()
#     token = login_data.get('access_token')  # Use .get() for safer access

#     # Ensure that the token is present
#     assert token, "Access token was not returned in the login response"

#     # Make authenticated request to the /users route
#     headers = {'Authorization': f'Bearer {token}'}
#     response = client.get('/users', headers=headers)
    
#     # Ensure the response is successful
#     assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
#     # Check if the response contains user data (assuming the response is a list of users)
#     users = response.get_json()
#     assert isinstance(users, list), "Expected the response to be a list of users"
#     assert len(users) > 0, "No users found"
#     assert 'user_id' in users[0], "User data does not contain 'user_id'"
#     assert 'first_name' in users[0], "User data does not contain 'first_name'"  # Additional checks based on your model
#     assert 'last_name' in users[0], "User data does not contain 'last_name'"
#     assert 'role' in users[0], "User data does not contain 'role'"

# def test_get_users(client, auth_headers):
#     # Send a GET request to retrieve the list of users with a valid JWT token
#     response = client.get('/users', headers=auth_headers)

#     # Assert that the status code is 200 (OK)
#     assert response.status_code == 200

#     # Assert that the returned list of users contains the created user
#     data = json.loads(response.data)
#     assert len(data) > 0  # Ensure at least one user is returned
#     assert data[0]['user_id'] == 1
#     assert data[0]['first_name'] == 'John'
#     assert data[0]['last_name'] == 'Doe'


def test_get_users_access_denied(client):
    # Send a GET request to retrieve the list of users without a valid token
    response = client.get('/users')

    # Assert that the status code is 401 (Unauthorized)
    assert response.status_code == 401

# def test_create_user(client):
#     # Data for creating a new user
#     user_data = {
#         'user_id': 4,
#         'role_code': 'admin',  # Assume this role exists in the roles table
#         'user_frst_name': 'John',
#         'user_last_name': 'Doe',
#         'user_login': 'johndoe',
#         'password': 'password123',
#         'other_details': 'Some details about the user',
#         'Roles_role_code': 1  # Assuming this maps to a valid role in the roles table
#     }

#     # Make a POST request to create a user
#     response = client.post('/users', json=user_data)

#     # Assert that the user is created successfully (status code 201)
#     assert response.status_code == 201
#     assert b'User created successfully' in response.data

def test_create_user_missing_fields(client):
    # Test missing required fields
    incomplete_data = {
        'role_code': 'admin',
        'user_frst_name': 'John',
        'user_last_name': 'Doe',
        'user_login': 'johndoe'
    }

    # Make a POST request with missing fields
    response = client.post('/users', json=incomplete_data)

    # Assert that the error message is returned for missing fields
    assert response.status_code == 400
    assert b'Missing field(s)' in response.data