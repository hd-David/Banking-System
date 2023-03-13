from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

def logout_required(f):
    """
    Decorator to ensure that only users who are not already logged in can access the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    Decorator to ensure that only authenticated users can access a route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function