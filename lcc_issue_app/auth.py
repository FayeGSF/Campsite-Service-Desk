# made this py file so the decorator can be referenced in route that requires
# user authentication and remove the need for individual role py file

from functools import wraps
from flask import request, redirect, url_for, session, flash,render_template


def login_required():
    # checks if user is logged in and has the correct role
    def decorator_login(f):
        @wraps(f)
        # when the route is accessed or denied
        def decorated_function (*args, **kwargs):
            if 'loggedin' not in session:   
                return redirect(url_for ('login', next=request.url))
            if session.get('status') == 'inactive':
                session.clear()
                flash("Your account is inactive. Please contact admin.","danger")
                return render_template ('login.html')
            return f(*args, **kwargs)
        return decorated_function
    return decorator_login

#top to bottom execution closest to function

def role_required(role):
    def decorator_role(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):  
            if session.get('role') != role:
                return redirect(url_for('home'))  # Redirect unauthorized users
            return f(*args, **kwargs)
        return wrapped_function
    return decorator_role
