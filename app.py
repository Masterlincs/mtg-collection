from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from main import fetch_and_store_cards
import asyncio
from flask_bcrypt import Bcrypt
import secrets
import os
from werkzeug.utils import secure_filename
from db import CardModel
from flask import Flask, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
bcrypt = Bcrypt(app)
SECRET_FILE_PATH = "flask_secret.txt"
try:
    with open(SECRET_FILE_PATH, "r") as secret_file:
        secret_key = secret_file.read()
        secret_key_hash = bcrypt.generate_password_hash(secret_key)
except FileNotFoundError:
    # Let's create a cryptographically secure code in that file
    with open(SECRET_FILE_PATH, "w") as secret_file:
        secret_key = secrets.token_hex(32)
        secret_file.write(secret_key)
        secret_key_hash = bcrypt.generate_password_hash(secret_key)
app.config['SECRET_KEY'] = secret_key_hash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DATABASE_URI = 'sqlite:///collection.db'  # Update this with your actual database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class UploadFileForm(FlaskForm):
    file = FileField('Card List File', validators=[DataRequired()])
    submit = SubmitField('Upload')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/fetch_and_store_cards', methods=['POST'])
def fetch_and_store_cards_route():
    data = request.get_json()
    set_codes = data.get('set_codes', [])
    card_nums = data.get('card_nums', [])
    asyncio.run(fetch_and_store_cards(set_codes, card_nums))
    return jsonify({"message": "Cards fetched and stored successfully."})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
async def upload():
    print(current_user.is_authenticated)
    form = UploadFileForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(file_path)

        await fetch_and_store_cards(file_path)
        
        flash('File uploaded and added to databse')
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form)

@app.route("/view_cards")
def view_cards():
    session = Session()
    result = session.execute(text("SELECT name FROM cards"))
    cards = result.fetchall()
    session.close()
    return render_template('view_cards.html', cards=cards)



if __name__ == '__main__':
    app.run(debug=True)