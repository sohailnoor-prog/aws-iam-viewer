"""Authentication routes."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.services.cognito_auth import CognitoAuthService

auth_bp = Blueprint('auth', __name__)
cognito_service = CognitoAuthService()


def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Validate token
        if not cognito_service.validate_token(session['access_token']):
            session.clear()
            flash('Your session has expired. Please log in again.', 'warning')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication handler."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        # Authenticate with Cognito
        tokens = cognito_service.authenticate_user(username, password)
        
        if tokens:
            # Create session
            session.permanent = True
            session['access_token'] = tokens.access_token
            session['id_token'] = tokens.id_token
            session['refresh_token'] = tokens.refresh_token
            session['username'] = username
            
            # Get user info
            user = cognito_service.create_user_from_token(tokens.access_token)
            if user:
                session['email'] = user.email
                session['cognito_sub'] = user.cognito_sub
            
            flash('Login successful!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')
    
    # GET request - show login form
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard after login."""
    return render_template('dashboard.html', username=session.get('username'))
