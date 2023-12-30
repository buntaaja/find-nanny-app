from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256
import os

app = Flask(__name__, template_folder='../frontend')

CORS(app, resources={r"/*": {'origins': "*"}}, supports_credentials=True)
#CORS(app)

app.config['SECRET_KEY'] = os.urandom(24)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ajnlz8i.@localhost/find_nanny'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

class User(UserMixin, db.Model): 
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    birthday_month = db.Column(db.Integer, nullable=False)  
    birthday_day = db.Column(db.String(10), nullable=False)    
    birthday_year = db.Column(db.Integer, nullable=False) 
    gender = db.Column(db.String(10), nullable=False) 

    def __init__(self, email, firstName, lastName, password, birthday_month, birthday_day, birthday_year, gender):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.birthday_month = birthday_month
        self.birthday_day = birthday_day
        self.birthday_year = birthday_year
        self.gender = gender

def valid_credentials(email, password):
    # Check credentials are valid
    user_object = User.query.filter_by(email=email).first()

    if user_object and pbkdf2_sha256.verify(password, user_object.password):
        return user_object

    return False

def validate_email(email):
    user_object = User.query.filter_by(email=email).first()
    if user_object: 
        return True
    return False    


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     # Handle API routes here
#     return jsonify({'status': 'error', 'message': 'API route not found'}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Handle all routes here
    return render_template("index.html")

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/register", methods=['POST'])
def register():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        app.logger.info('Received data: %s', post_data)
        firstName = post_data.get('firstName')
        lastName = post_data.get('lastName')
        email = post_data.get('email')
        password = post_data.get('password')
        confirm_password = post_data.get('confirm_password')
        birthday_month = post_data.get('birthday_month')
        birthday_day = post_data.get('birthday_day')
        birthday_year = post_data.get('birthday_year')
        gender = post_data.get('gender')

        response_object['message'] = "An unexpected error occurred."

        if (
            firstName == ''
            or lastName == ''
            or email == ''
            or password == ''
            or confirm_password == ''
            or birthday_month == ''
            or birthday_day == ''
            or birthday_year == ''
            or gender == ''
        ):
            response_object['message'] = "Please enter required fields."
            return jsonify(response_object), 400  # 400 Bad Request status

        if validate_email(email):
            response_object['message'] = 'Email already exists'
            return jsonify(response_object), 409  # 409 Conflict status

        if password == confirm_password and 30 >= len(password) >= 4:
            hashed_pswd = pbkdf2_sha256.hash(password)
            user = User(
                email=email,
                firstName=firstName,
                lastName=lastName,
                password=hashed_pswd,
                birthday_month=birthday_month,
                birthday_day=birthday_day,
                birthday_year=birthday_year,
                gender=gender,
            )
            db.session.add(user)
            db.session.commit()
            response_object['message'] = "Registered successfully. Now you can log in."
            return jsonify(response_object), 200  # 200 OK status

    # If it's not a POST request, provide a different response
    response_object['message'] = "Invalid request method. Please use POST."
    return jsonify(response_object), 405  # 405 Method Not Allowed status

@app.route("/login", methods=['GET', 'POST'])
def login_route():
    response_object = {'status': 'error', 'message': 'Invalid email or password'}
    if request.method == 'POST':
        post_data = request.get_json()
        email = post_data.get('email')
        print(email)
        password = post_data.get('password')

        user_object = valid_credentials(email, password)
        print(user_object)
    
        if user_object:
            login_user(user_object)
            response_object['status'] = 'success'
            response_object['message'] = 'Logged in.'
        
    return jsonify(response_object)

@app.route("/logout", methods=['GET'])
def logout():
    response_object = {'status': 'success', 'message': 'Logged out successfully.'}
    logout_user()
    return jsonify(response_object)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)