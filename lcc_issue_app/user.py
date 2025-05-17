from lcc_issue_app import app
from lcc_issue_app import db
from flask import redirect, url_for,request,session,render_template
from flask_bcrypt import Bcrypt
import re
from lcc_issue_app.auth import login_required, role_required

# create RBAC routes for admin and helper
@app.route('/admin_dashboard')
@login_required()
@role_required ('admin') # Only accessible by admins
def admin_dashboard():
    username=session.get('username')
    if username is None:
        return redirect(url_for('login'))  # Or redirect to an appropriate page
    return render_template('admin_dashboard.html', username=username)

@app.route('/helper_dashboard')
@login_required()
@role_required('helper') # Only accessible by helpers
def helper_dashboard():
    return render_template('helper_dashboard.html')


@app.route('/visitor_dashboard')
@login_required()
@role_required ('visitor')# Only accessible by visitor
def visitor_dashboard():
    username=session.get('username')
    return render_template('visitor_dashboard.html', username=username)