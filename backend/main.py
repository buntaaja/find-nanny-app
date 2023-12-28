from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy, or_
from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

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

def invalid_credentials(form, field):
    email_entered = request.form['email'] 
    password_entered = request.form['password'] 

    # Check credentials are valid
    user_object = User.query.filter_by(email=email_entered).first()
    
    if user_object is None:
        raise ValidationError("Email or password is incorrect.")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Email or password is incorrect")

def validate_email(form):
    email_entered = request.form['email'] 
    user_object = User.query.filter_by(email=email_entered).first()
    if user_object: 
        raise ValidationError("This email adress is already in use.")        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", form=reg_form)

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        firstName = request.form['firstName'] # The name of the input in index.html
        firstName = request.form['lastName'] 
        email = request.form['email']
        password = request.form['password']
        confirm_pasword = request.form['confirm_pasword']
        birthday_month = request.form['birthday_month']
        birthday_day = request.form['birthday_day'] 
        birthday_year = request.form['birthday_year']
        gender = request.form['gender']

        if customer == '' or dealer == '':
            return render_template('index.html', message='Plase enter required fields')

    # Update DB if validation was successfull
    if reg_form.validate_on_submit():
        email = reg_form.email.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password) 

        # Add user to DB
        user = User(email=email, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered succesfully. Please login.', 'success') 
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username_email = login_form.username_email.data
        password = login_form.password.data

        user_object = User.query.filter(or_(User.username == username_email, User.email == username_email)).first()

        if user_object and user_object.check_password(password):
            login_user(user_object)
            return redirect(url_for('choose'))

    return render_template("login.html", form=login_form)

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