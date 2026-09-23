# utils.py

from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    """
    Decorator to restrict access to a route to only users with the 'admin' role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in AND if their role is 'admin'
        if 'loggedin' not in session or session.get('role') != 'admin':
            flash('Access denied. Administrators only.', 'danger')
            # Redirect to login page
            return redirect(url_for('auth.login_page')) 
        return f(*args, **kwargs)
    return decorated_function