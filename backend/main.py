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
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

def invalid_credentials(form, field):
    email_entered = form.email.data
    username_entered = form.username.data
    password_entered = field.data

    # Check credentials are valid
    user_object = User.query.filter_by(username=username_entered).first()
    user_object_email = User.query.filter_by(email=email_entered).first()

    if user_object is None or user_object_email is None:
        raise ValidationError("Username or password is incorrect.")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    username = StringField('username_label', 
        validators=[InputRequired(message="Username required"),
        Length(min=4, max=30, message="Username must be between 4 and 30 characters")])
    email = StringField('email_label', validators=[InputRequired(message="Email required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=30, message="Password must be between 4 and 30 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')
    
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select different username.")

    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object: 
            raise ValidationError("This email adress is already in use.")        

class LoginForm(FlaskForm):
    username_email = StringField('Username or Email', 
        validators=[InputRequired(message="Username or email required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        invalid_credentials])
    submit_button = SubmitField('Login')


@login.user_loader
def load_user(id):

    # User.query.filter_by(id=id).first()
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Update DB if validation was successfull
    if reg_form.validate_on_submit():
        email = reg_form.email.data
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password) 

        # Add user to DB
        user = User(email=email, username=username, password=hashed_pswd)
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