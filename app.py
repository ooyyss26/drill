from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/access_control'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'

    if config:
        app.config.update(config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    register_error_handlers(app)

    return app

# Register routes
def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Users Access Control',
            'endpoints': {
                '/users': 'Manage users',
            }
        })
    
# Register error handlers
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        # Assume we check user credentials here
        username = data.get('username')
        password = data.get('password')

        # In a real app, you would validate the user against the database
        if username == 'admin' and password == 'admin':
            access_token = create_access_token(identity=username, additional_claims={'role': 'admin'})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/users', methods=['GET'])
    @jwt_required()
    def get_users():
        claims = get_jwt()  # Get the full claims from the JWT
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Access forbidden: You do not have the required role'}), 403

        users = User.query.all()
        return jsonify([{
            'user_id': u.user_id,
            'first_name': u.user_frst_name,
            'last_name': u.user_last_name,
            'login': u.user_login,
            'role': u.role.role_description
        } for u in users])
    
    @app.route('/users/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        claims = get_jwt()  # Get the full claims from the JWT
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Access forbidden: You do not have the required role'}), 403

        # Retrieve the user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user_id': user.user_id,
            'first_name': user.user_frst_name,
            'last_name': user.user_last_name,
            'login': user.user_login,
            'role': user.role.role_description
        })



class Facility(db.Model):
    __tablename__ = 'facilities'

    facility_id = db.Column(db.Integer, primary_key=True)
    facility_type_code = db.Column(db.String(45), nullable=False)
    access_count = db.Column(db.String(45), nullable=False)
    facility_name = db.Column(db.String(45), nullable=False)
    facility_description = db.Column(db.String(45), nullable=False)
    other_details = db.Column(db.String(45), nullable=False)
    Ref_Facility_Types_facility_type_code = db.Column(db.Integer, db.ForeignKey('ref_facility_types.facility_type_code'), nullable=False)

    ref_facility_type = db.relationship('RefFacilityType', backref='facilities')


class FacilityFunctionalArea(db.Model):
    __tablename__ = 'facility_functional_areas'

    functional_area_code = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.String(45), nullable=False)
    Functional_Areas_functional_area_code = db.Column(db.Integer, db.ForeignKey('functional_areas.functional_area_code'), nullable=False)
    Facilities_facility_id = db.Column(db.Integer, db.ForeignKey('facilities.facility_id'), nullable=False)

    facility = db.relationship('Facility', backref='functional_areas')
    functional_area = db.relationship('FunctionalArea', backref='facility_areas')


class FunctionalArea(db.Model):
    __tablename__ = 'functional_areas'

    functional_area_code = db.Column(db.Integer, primary_key=True)
    parent_functional_area_code = db.Column(db.String(45), nullable=False)
    functional_area_description = db.Column(db.String(45), nullable=False)
    eg_HR_Finance = db.Column(db.String(45), nullable=False)
    Functional_Areas_functional_area_code = db.Column(db.Integer, db.ForeignKey('functional_areas.functional_area_code'), nullable=False)

    parent_functional_area = db.relationship('FunctionalArea', remote_side=[functional_area_code], backref='child_functional_areas')


class RefFacilityType(db.Model):
    __tablename__ = 'ref_facility_types'

    facility_type_code = db.Column(db.Integer, primary_key=True)
    facility_type_description = db.Column(db.String(45), nullable=False)
    eg_Menus_Records_Screens = db.Column(db.String(45), nullable=False)


class RoleFacilityAccessRight(db.Model):
    __tablename__ = 'role_facility_access_rights'

    facility_id = db.Column(db.Integer, primary_key=True)
    role_code = db.Column(db.String(45), nullable=False)
    CRUD_Value = db.Column(db.String(45), nullable=False)
    eg_R_RW = db.Column(db.String(45), nullable=False)
    Facilities_facility_id = db.Column(db.Integer, db.ForeignKey('facilities.facility_id'), nullable=False)
    Roles_role_code = db.Column(db.Integer, db.ForeignKey('roles.role_code'), nullable=False)

    facility = db.relationship('Facility', backref='role_access_rights')
    role = db.relationship('Role', backref='facility_access_rights')


class Role(db.Model):
    __tablename__ = 'roles'

    role_code = db.Column(db.Integer, primary_key=True)
    role_description = db.Column(db.String(45), nullable=False)
    eg_DBA_Project_Mgr = db.Column(db.String(45), nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    role_code = db.Column(db.String(45), nullable=False)
    user_frst_name = db.Column(db.String(45), nullable=False)
    user_last_name = db.Column(db.String(45), nullable=False)
    user_login = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    other_details = db.Column(db.String(45), nullable=False)
    Roles_role_code = db.Column(db.Integer, db.ForeignKey('roles.role_code'), nullable=False)

    role = db.relationship('Role', backref='users')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)