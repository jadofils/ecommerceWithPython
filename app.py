from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Routes for user registration and login
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register_user'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Updated method
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login_user'))
        except Exception as e:
            db.session.rollback()
            flash("Error: " + str(e))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!")
            return redirect(url_for('admin_page'))
        else:
            flash("Invalid email or password")

    return render_template('login.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login_user'))
    
    return render_template('admin.html')

# Other routes for the application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/order_history')
def order_history():
    return render_template('order_history.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

if __name__ == '__main__':
    app.run(debug=True)
