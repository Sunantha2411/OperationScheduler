from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, firestore, auth
import logging

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'Sunantha@2411'  # Change this to a real secret key for production

# Load the service account key JSON file
cred = credentials.Certificate('firebase_admin_config.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Logging setup
logging.basicConfig(filename='app.log', level=logging.INFO)

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# Function to Register User
@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        password = request.form['password']
        # Create a new user in Firebase Authentication
        user = auth.create_user(email=email, password=password)
        # Save user details to Firestore
        db.collection('users').document(user.uid).set({
            'email': email,
            'role': 'user'  # default role is user
        })
        logging.info(f"New user registered: {email}")
        flash('Registration successful', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        flash('Registration failed', 'danger')
        return redirect(url_for('index'))

# Function to Login User
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        # Check if user exists
        user = auth.get_user_by_email(email)
        if user:
            # For Firebase Authentication, you would use Firebase's client SDK or REST API to verify password
            # This example assumes the password is 'testpassword', which is insecure
            # You should use Firebase Authentication to handle this securely
            if password == 'testpassword':  # This should be replaced with actual password verification
                session['user_id'] = user.uid
                logging.info(f"User logged in: {email}")
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid credentials', 'danger')
                return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        flash('Login failed', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
