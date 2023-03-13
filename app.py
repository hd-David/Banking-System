from flask import *
from forms import *
from model import *
from decorators import *
import os
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from flask_login import login_user, LoginManager



app = Flask(__name__)

Session = dbconnect()
#CSRFProtect(app)
login_manager = LoginManager(app)

SECRET_KEY = os.urandom(64)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get username or email and password from form
        email = form.email.data
        password = form.password.data

        # Check if user exists and password is correct
        user = Session.query(Customer).filter(Customer.email == email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # Log the user in
        login_user(user)
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if a customer with the same email already exists in the database
        existing_customer = Session.query(Customer).filter_by(email=form.email.data).first()
        if existing_customer:
            flash('Email already exists')
            return redirect(url_for('register'))

        # Check if a customer with the same username already exists in the database
        existing_customer = Session.query(Customer).filter_by(username=form.username.data).first()
        if existing_customer:
            flash('Username already exists')
            return redirect(url_for('register'))

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(form.password.data)

        # Create a new customer object and add it to the database
        customer = Customer(
            name=form.name.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            username=form.username.data,
            password=hashed_password
        )
        Session.add(customer)
        Session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # Get the current user's ID from the session
    user_id = session.get('user_id')

    # Get the user's account information from the database
    user_account = Session.query(Account).filter_by(user_id=user_id).first()

    # Get the user's transaction history from the database
    transactions = Session.query(Transaction).filter_by(account_id=user_account.id).all()

    # Get the user's name and email address from the database
    user = Session.query(Customer).filter_by(id=user_id).first()
    name = user.name
    email = user.email

    # Calculate the user's account balance
    balance = user_account.balance

    # Render the dashboard template with the user's information
    return render_template('index.html', name=name, email=email, balance=balance, transactions=transactions)




if __name__ == '__main__':
    app.run(debug=True)
