from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy, or_
from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

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
    password = db.Column(db.String(30), nullable=False)
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
        return user_object
    return False    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        firstName = request.form['firstName'] # The name of the input in index.html
        lastName = request.form['lastName'] 
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birthday_month = request.form['birthday_month']
        birthday_day = request.form['birthday_day'] 
        birthday_year = request.form['birthday_year']
        gender = request.form['gender']

        if firstName == '' or lastName == '' or email == '' or password == '' or confirm_password == '' or birthday_month == '' or birthday_day == '' or birthday_year == '' or gender == '':
            return render_template('register.html', message='Plase enter required fields')

        if not validate_email(email):
            return render_template('login.html', message='Email or password is incorrect')

        elif validate_email(email) and password == confirm_password and 30 >= len(password) >= 4:
            # Hash password
            hashed_pswd = pbkdf2_sha256.hash(password) 

            # Add user to DB
            user = User(email=email, password=hashed_pswd)
            db.session.add(user)
            db.session.commit()

            flash('Registered succesfully. Please login.', 'success') 
            return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_object = valid_credentials(email, password)
    
        if not user_object:
            return render_template('login.html', message='Email or password is incorrect')
        else:
            login_user(user_object)
            return redirect(url_for('choose'))

    return render_template("login.html")

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route("/choose", methods=['GET', 'POST'])
#@login_required
def choose():
    return render_template('choose.html', username=current_user.username)


if __name__ == "__main__":
    app.run(debug=True)