**Users Access Control Application**  
**Description**

This project is a user access control application built using Flask. It allows for creating, reading, updating, and deleting users, along with managing roles, facilities, and access rights. The application uses SQLAlchemy for database management and Flask-JWT-Extended for secure authentication.

**Installation**

To install the necessary dependencies, run the following command:

pip install \-r requirements.txt

**Configuration**

The application requires the following configurations:

* **SQLALCHEMY\_DATABASE\_URI**: Connection string for your MySQL database.  
* **JWT\_SECRET\_KEY**: A secret key for securing JWT tokens.

**Example configuration in the `create_app` function:**

app.config\['SQLALCHEMY\_DATABASE\_URI'\] \= 'mysql+pymysql://\<username\>:\<password\>@\<host\>/\<database\>'  
app.config\['JWT\_SECRET\_KEY'\] \= 'your-secret-key'

**API Endpoints**

| HTTP Method | Endpoint | Description | Requirements |
| ----- | ----- | ----- | ----- |
| **GET** | `/` | Returns a welcome message and available endpoints. | None |
| **POST** | `/login` | Authenticates a user and returns a JWT token if valid. | None |
| **GET** | `/users` | Retrieves a list of all users. | JWT required, "admin" role |
| **GET** | `/users/<int:user_id>` | Retrieves details of a specific user by ID. | JWT required, "admin" role |
| **POST** | `/users` | Creates a new user. | None explicitly mentioned |
| **PUT** | `/users/<int:user_id>` | Updates details of a specific user by ID. | None explicitly mentioned |
| **DELETE** | `/users/<int:user_id>` | Deletes a user and related access rights. | None explicitly mentioned |

**Testing**

To run the tests, execute the following command:

pytest app\_test.py

**Test Highlights**

* **`test_home`**: Validates the home route response.  
* **`test_get_users`**: Tests retrieving users with valid JWT.  
* **`test_get_users_access_denied`**: Tests access denial when JWT is not provided.  
* **`test_create_user`**: Verifies user creation functionality.  
* **`test_update_user`**: Checks if user details can be updated.  
* **`test_delete_user`**: Ensures users can be deleted successfully.

**Database Models**

The application includes the following models:

* **User**: Stores user information and is linked to roles.  
* **Role**: Defines user roles and permissions.  
* **Facility**: Represents facilities with access details.  
* **FacilityFunctionalArea**: Links facilities to functional areas.  
* **FunctionalArea**: Represents functional areas such as HR and Finance.  
* **RefFacilityType**: Stores facility type references.  
* **RoleFacilityAccessRight**: Defines access rights for roles on facilities.

**Git Commit Guidelines**

Use conventional commit messages for better tracking. Examples:

feat: add login functionality  
fix: resolve user creation error  
docs: update testing instructions  
test: add test for user deletion

**Additional Notes**

* Ensure the database is initialized before starting the application.  
* Error handling is in place for common HTTP errors (e.g., `404`, `500`).  
* The project uses Flask-JWT-Extended for secure token-based authentication.

