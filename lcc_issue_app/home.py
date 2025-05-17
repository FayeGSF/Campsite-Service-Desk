from lcc_issue_app import app
from lcc_issue_app import db
from flask import redirect, url_for,request,session,render_template,flash,Request
from flask_bcrypt import Bcrypt
import re
from lcc_issue_app.auth import login_required
import datetime
import os

flask_bcrypt =Bcrypt(app)
# defined some default variables
DEFAULT_USER_ROLE='visitor'
DEFAULT_USER_STATUS='active'
DEFAULT_ISSUE_STATUS='new'

# IMAGE  function- defining path and the allowed extensions
app.config['IMAGE_UPLOADS']=os.path.join("lcc_issue_app","static","profile_pic")
app.config['ALLOWED_IMAGE_EXTENSIONS']=['png','jpg','jpeg','gif']

# ensure profile pic extension and file name is checked. 
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1].lower()
    if ext in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else: 
        return False
    
    
# remove profile picture function that will be called in update_profile route
def remove_image(user_profile):
    user_id= user_profile.get('user_id')
    # check if there is an existing profile pic
    profile_img_filename =user_profile.get("profile_image")
    if profile_img_filename:
        os.remove (os.path.join(app.config['IMAGE_UPLOADS'],profile_img_filename))
        user_profile["profile_image"]=None
    with db.get_cursor() as cursor:
        cursor.execute('''UPDATE users SET profile_image =NULL 
                       WHERE user_id=%s''',(user_id,))
        
    

# homepage/landing page
@app.route('/')
def home_page():
    return render_template('landingpage.html')


# a route once logged in
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST" and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        # retrieve details from db
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT 
                           user_id,username, password_hash,role,status
                           FROM users WHERE username=%s''',(username,))
            account= cursor.fetchone()
        if account is None:
            return render_template('login.html', 
                                   username=username, username_invalid=True,
                                   password_invalid=True)
         # if a user is "inactive" they are not allowed to login
        session['status'] = account['status']
        if account['status'] == 'inactive':
                session['loggedin']=False
                flash(" Your account is inactive, please contact admin."),403
                return redirect(url_for('login'))
        # if matched account found
        if account is not None:
        #Check if username is in db
            db_username = account['username']
            if username == db_username:       
        # check if password matches the hash
        # if it matches, create a session and go to role-dashboard page
        # else, error and stay on login page
                password_hash=account['password_hash']
                if flask_bcrypt.check_password_hash(password_hash, password):
                    session['loggedin']=True
                    session['user_id']=account['user_id']
                    session['username']=account['username']
                    session['role']=account['role']
                    session['status']=account['status']
                # Once logged in, user will be redirected to 
                # dashboard based on their role
                    if session['role']=='visitor':
                        return redirect (url_for('visitor_dashboard'))
                    elif session['role']== 'admin':
                        return redirect(url_for('admin_dashboard'))
                    elif session['role']=='helper':
                        return redirect(url_for('helper_dashboard'))
                    else:
                        return redirect (url_for('login'))
            # If password does not match db 
                else:
                    return render_template('login.html', username=username, password_invalid=True)
            else:
                return render_template ('login.html', username=username, username_invalid=True)
        #if no account was found, return to login page
        else:
            return render_template('login.html', username=username, password_invalid=True,username_invalid =True)
    return render_template('login.html')


# register page
@app.route('/register', methods=['GET','POST'])
def register():
    # check if all required fields are filled
    if request.method=="POST":
        firstname = request.form.get ('firstname')
        lastname = request.form.get ('lastname')
        username = request.form.get ('username')
        email = request.form.get ('email')
        password = request.form.get ('password')
        passwordconfirm=request.form.get('passwordconfirm')
        location=request.form.get('location')

        username_error = None
        email_error = None
        password_error = None

        #check if username already exists in db
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT 
                           username, email 
                           FROM users WHERE username=%s;''',(username,))
            username_already_exists=cursor.fetchone() is not None
        # Check username constraints:
        # -unique username
        # -no longer than 20 characters
        # -username only contains letters and numbers, not symbols
        if username_already_exists:
            username_error = 'An account with the username already exists.'
        elif len(username or "")> 20:
            username_error = 'Username cannot exceed 20 Characters'
        elif not re.fullmatch(r'[A-Za-z0-9]+', username):
            username_error = 'Username can only contain letters and numbers'     
        #Check email contraints:
        # -valid email with a @, not ..com, domain is present, com is present
        # -email len no longer than 320
        if len(email) >320:
            email_error = 'Your email must not exceed 320 characters'
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',email):
            email_error = 'Email is invalid.'
        #Check password constraints:
        # -password and passwordcondirm must match
        # -password more than 8 characters
        # -mix type characters (special char, number, alphabets) in passwords
        if password != passwordconfirm:
            password_error = 'The passwords do not match.'
        elif len(password)< 8:
            password_error = 'Password must be at least 8 characters.'
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$', password):
            password_error = 'Password must contain at least 1 special character and number'
        # If constraints are not met or errors occur
        # return to register page but keep the populated fields (exl.password)
        if (password_error or email_error or username_error):
            return render_template ('register.html', username=username, 
                                    email=email, location=location,
                                    firstname=firstname,lastname=lastname,
                                    username_error=username_error,
                                    password_error=password_error,
                                    email_error=email_error)
        else:
            password_hash=flask_bcrypt.generate_password_hash(password)
        with db.get_cursor() as cursor:
            cursor.execute('''INSERT INTO users 
                           (username,password_hash,email, first_name,last_name,
                           location,role,status)
                           VALUES(%s,%s,%s,%s,%s,%s,%s,%s);
                           ''', (username,password_hash,email,firstname,lastname,
                                 location,
                                 DEFAULT_USER_ROLE,DEFAULT_USER_STATUS))
        flash ('Registered successfully!','success')
        return redirect(url_for('home_page'))
    return render_template ('register.html')

# route to post issues
@app.route('/post_issue', methods=['GET','POST'])
@login_required()
def post_issue():
    if request.method=="POST":
        role=session.get('role')
        username=session.get('username')
        user_id=session.get('user_id')
        summary=request.form.get ('summary')
        description=request.form.get('description')
        status=request.form.get('issue_status', DEFAULT_ISSUE_STATUS)
        timestamp= datetime.datetime.now()
        created_at = timestamp.strftime("%Y-%m-%d %X")
        with db.get_cursor() as cursor:
            cursor.execute('''INSERT INTO issues 
                        (user_id,summary,description,created_at,status)
                        VALUES (%s, %s, %s, %s,%s);''',(user_id,summary,description,created_at,status,))
        new_issue_id=cursor.lastrowid
        flash("Issue has been reported successfully!",'success')
        return redirect (url_for('issue_detail', id=new_issue_id))
    return render_template ('post_issue.html')


# modify/view issue details
@app.route('/issue_detail', methods=['GET','POST'])
@login_required()
def issue_detail():
    #only users can see the posts that they made
    user_id=session.get('user_id')
    issue_id=request.args.get('id')
    with db.get_cursor() as cursor:
        cursor.execute ('''SELECT i.issue_id, i.user_id, u.username, u.role,
                        i.summary, i.description,i.created_at, i.status
                        FROM issues AS i
                        INNER JOIN users AS u ON i.user_id = u.user_id 
                        WHERE i.issue_id = %s;  ''',(issue_id,))
        issue_detail=cursor.fetchone()
        if not issue_detail:
                flash("Issue not found!",'danger')
                return redirect(url_for('view_issues'))
    with db.get_cursor() as cursor:
    # display comments of issue_id
        cursor.execute ('''SELECT c.comment_id, c.issue_id,c.user_id,
                         u.username,u.role, c.context, c.created_at, i.status,u.profile_image
                        FROM  comments AS c
                        INNER JOIN issues as i on c.issue_id = i.issue_id 
                        INNER JOIN users as u on c.user_id = u.user_id
                        WHERE c.issue_id=%s
                        ;''',(issue_id,))
        comments = cursor.fetchall()
    # if there are no comments on the issue, display no comments.
    if not comments:
        no_comment_message="No comments"
    else:
        no_comment_message="None"
    return render_template ('issue_detail.html', issue_detail=issue_detail, 
                            issue_id=issue_id, user_id=user_id, comments=comments,
                             no_comment_message = no_comment_message )


@app.route('/update_issue', methods=['GET','POST'])
@login_required()
def update_issue():
    #update issues which should only be accessible to admin,helper 
    user_id=session.get('user_id')
    issue_id=request.args.get('id')
    issue_status = request.form.get('issue_status')
    with db.get_cursor() as cursor:
        cursor.execute ('''UPDATE issues
                        set status =%s
                        WHERE issue_id=%s;  ''',(issue_status,issue_id,))
    # display issue once updated
    with db.get_cursor() as cursor:
        cursor.execute ('''SELECT i.issue_id, i.user_id, u.username, u.role,
                        i.summary, i.description,i.created_at, i.status
                        FROM issues AS i
                        INNER JOIN users AS u ON i.user_id = u.user_id 
                        WHERE i.issue_id = %s;  ''',(issue_id,))
        issue_detail=cursor.fetchone()
    with db.get_cursor() as cursor:
    # display comments of issue_id
        cursor.execute ('''SELECT c.comment_id, c.issue_id,c.user_id,
                         u.username,u.role, c.context, c.created_at, i.status,u.profile_image
                        FROM  comments AS c
                        INNER JOIN issues as i on c.issue_id = i.issue_id 
                        INNER JOIN users as u on c.user_id = u.user_id
                        WHERE c.issue_id=%s
                        ;''',(issue_id,))
        comments = cursor.fetchall()
        flash('Issue has been updated.','success')
    return render_template ('issue_detail.html', issue_detail=issue_detail,
                             issue_id=issue_id, issue_status=issue_status, 
                             comments=comments, user_id=user_id )


# route to add comments
@app.route('/add_comment', methods=['GET','POST'])
@login_required()
def add_comment():
    user_id=session.get('user_id')
    user_role=session.get('user_role')
    issue_id=request.form.get('issue_id')
    context=request.form.get('context')
    #retrieving the user_id that authored the issue 
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT i.issue_id, i.user_id, u.username, u.role,
                        i.summary, i.description,i.created_at, i.status
                        FROM issues AS i
                        INNER JOIN users AS u ON i.user_id = u.user_id 
                        WHERE i.issue_id = %s
                        ;''',(issue_id,))
        issue_detail=cursor.fetchone()
        if not issue_detail:
            flash("Issue not found!",'danger')
            return redirect(url_for('issue_detail', id=issue_id))
    
        issue_user_id= issue_detail['user_id']
        issue_status = issue_detail['status']
    # adding role restriction to visitor and user_id check 
    if user_role != 'visitor' or issue_user_id == user_id:
        with db.get_cursor() as cursor:
            cursor.execute ('''INSERT INTO comments (issue_id, user_id, context
                            )
                           VALUES (%s,%s,%s);''',
                        (issue_id,user_id,context,))
    #if user role == admin/ helper adds comment, update issue_status to open 
    if session.get('role') in ['admin','helper'] and issue_status in['new','stalled','resolved']:
        with db.get_cursor() as cursor:
            cursor.execute('''UPDATE issues SET status = 'open'
                        WHERE issue_id=%s;''',(issue_id,))
        flash('Comment added, issue status has been updated!','success')
    # visitor can add comment but status will not change. 
    else:
        flash('Comment added successfully!','success')
    return redirect(url_for('issue_detail', id=issue_id))
    

# only when loggedin, all issues can be viewed
@app.route('/view_issues', methods=['GET'])
@login_required()
def view_issues():
    #only visitors can see the posts that they made (incl resolved issues)
    if session.get('role') =='visitor':
        user_id=session.get('user_id')
        with db.get_cursor() as cursor:
            cursor.execute ('''SELECT i.issue_id, i.user_id, u.username, 
                            i.summary, i.description,i.created_at, i.status
                            FROM issues AS i
                            INNER JOIN users AS u ON i.user_id = u.user_id 
                            AND i.user_id= %s
                            ORDER by status, created_at DESC;  ''',(user_id,))
            issues=cursor.fetchall()
    #  admin and helpers can view all issues (excl- resolved)
    else:
        with db.get_cursor() as cursor:
            cursor.execute ('''SELECT i.issue_id, i.user_id, u.username, 
                            i.summary, i.description,i.created_at, i.status
                            FROM issues AS i
                            INNER JOIN users AS u ON i.user_id = u.user_id 
                            WHERE NOT i.status = 'resolved'
                            ORDER by status, created_at DESC;  ''')
            issues=cursor.fetchall()
    user_id= None        
    # if they have made 0 posts, message pops up
    if not issues:
        no_issues_message="No reported issues."
    else:
        no_issues_message="None"
    for issue in issues:
        issue['created_at']=issue['created_at'].strftime('%d/%m/%Y %H:%M:%S')
    return render_template ('view_issues.html', issues=issues, user_id=user_id,no_issues_message=no_issues_message)


@app.route('/resolved_issues', methods=['GET'])
@login_required()
def resolved_issues():
    # visitor should not be able to view this page.
    # adding it a safeguard if they have the link
    if session.get('role') =='visitor':
        return render_template ('access_denied.html')
    else:
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT i.issue_id, i.user_id, u.username, 
                            i.summary, i.description,i.created_at, i.status
                            FROM issues AS i
                            INNER JOIN users AS u ON i.user_id = u.user_id 
                            WHERE i.status = 'resolved'
                            ORDER BY created_at, i.issue_id DESC;''')
            resolved_issues =cursor.fetchall()
    return render_template ('resolved_issues.html', resolved_issues=resolved_issues)


# view user profile
@app.route('/user_profile', methods=['GET'])
@login_required()
def user_profile():
       user_id=session.get('user_id')
       with db.get_cursor() as cursor:
        cursor.execute('''SELECT * FROM users
                        WHERE user_id= %s;''',(user_id,))
        user_profile = cursor.fetchone()
        if not user_profile:
            return "User not found",404
        return render_template ('user_profile.html', user_profile=user_profile)


# profile updates
@app.route('/update_profile', methods=['GET','POST'])
@login_required()
def update_profile ():
    # view user profile
    user_id=session.get('user_id')
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT * FROM users WHERE user_id = %s;''', (user_id,))
        user_profile = cursor.fetchone()
# IMAGE
    # make changes to their profile - email, firstname, lastname, location, profile pic
    if request.method=="POST":
        first_name = request.form.get ('first_name')
        last_name = request.form.get ('last_name')
        email = request.form.get ('email')
        location= request.form.get('location')
        # if profile pic is existing, set image error as None
        profile_img_filename =user_profile.get("profile_image")
        profile_img_error=None
        profile_img= request.files.get('profile_img')
        # if profile pic is uploaded(filename, filetype)
        if profile_img:
            if not allowed_image(profile_img.filename):
                profile_img_error="Image extension is not allowed."
            # processing the uploaded file with defined filename convension
            # if profile_img and profile_img_filename and not profile_img_error:
            else:
                ext = profile_img.filename.rsplit(".", 1)[1].lower()
                # rename the file image with user_id
                filename=f"user_{user_id}.{ext}"
                filepath= os.path.join(app.config['IMAGE_UPLOADS'],filename)
                # check if directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                # save picture in directory defined in app.config - lcc_issue_app/static/profile_pic
                profile_img.save(filepath)
                profile_img_filename= filename
        
        # if user wants to remove profile pic
        if 'remove_pic' in request.form:
            # user the function remove_image and flash that it has been removed
            remove_image(user_profile)
            flash('Profile picture has been removed.', 'success')
            return redirect(url_for('user_profile'))
            
        email_error = None 
    #Check email contraints:
        # -valid email with a @, not ..com, domain is present, com is present
        # -email len no longer than 320
        if len(email) >320:
            email_error = 'Your email must not exceed 320 characters'
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',email):
            email_error = 'Email is invalid.'
        if email_error or profile_img_error :
             with db.get_cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE user_id=%s;', (user_id,))
                user_profile = cursor.fetchone()
                return render_template ('user_profile.html', 
                                    user_profile = user_profile,
                                    first_name=first_name, 
                                    last_name=last_name,
                                    email=email,
                                    location=location, 
                                    profile_img_error= profile_img_error,
                                    email_error=email_error )
    # Update profile 
        with db.get_cursor() as cursor:
            cursor.execute('''UPDATE users SET first_name=%s, last_name=%s, profile_image=%s,
                        email=%s, location=%s
                        WHERE user_id=%s;''',(first_name,last_name, profile_img_filename,
                                                email,location, user_id))
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT * FROM users WHERE user_id = %s;''', (user_id,))
            user_profile = cursor.fetchone()
        flash('Profile has been updated!','success')
   
        return render_template('user_profile.html', user_profile=user_profile )
    return render_template('user_profile.html', user_profile=user_profile)


# Change password 
@app.route('/update_password', methods=['GET','POST'])
@login_required()
def update_password ():
    user_id=session.get('user_id')
    if request.method=='POST':
        current_password = request.form.get ('current_password')
        current_password_confirm=request.form.get('current_password_confirm')
        new_password = request.form.get('new_password')
        new_password_confirm = request.form.get('new_password_confirm')

        password_error = None
        new_password_error= None
    #Check password constraints:
        #-current_password and current_password_confirm must match
        if current_password != current_password_confirm:
            password_error = 'Current passwords do not match.'
        # -new_password and new password_confirm must match
        elif new_password != new_password_confirm:
            new_password_error = 'New passwords do not match.'
        elif new_password == current_password:
            new_password_error = 'New password cannot be the same as current password. Try again.'
    # -passwords more than 8 characters    
        elif len(new_password)< 8:
            new_password_error = 'Password must be at least 8 characters.'
    # -mix type characters (special char, number, alphabets) in passwords
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$', new_password):
            new_password_error = 'Password must contain at least 1 special character and number'
    #  if there are errors with either new/current password, return to update_password page
        if password_error or new_password_error:
            return render_template ('update_password.html', 
                                    new_password_error=new_password_error,
                                    password_error=password_error)
            # check current_password with password_hash in db
    # check if current password is correct in database
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT password_hash FROM users
                            WHERE user_id=%s;''',(user_id,))
            user_password_hash=cursor.fetchone()

        if not user_password_hash or not flask_bcrypt.check_password_hash(user_password_hash['password_hash'], current_password):
            password_error= 'Current password is incorrect.'
            return render_template ('update_password.html', 
                                    password_error=password_error)

        #create new hash for new password and update it onto the db
        new_password_hash=flask_bcrypt.generate_password_hash(new_password)
        with db.get_cursor() as cursor:
            cursor.execute('''UPDATE users SET password_hash=%s 
                            WHERE user_id=%s''',(new_password_hash,user_id))
        flash('Password updated successfully.','success')
        return redirect(url_for('update_password'))
    return render_template('update_password.html')


#change user status (active/inactive) and user role - Admin access only
# View all users & profile (admin access only) 
@app.route('/all_users', methods=['GET','POST'])
@login_required()
def all_users():
    user_role=session.get('role')
    #display all users (id, username, role, status)
    if user_role == 'admin':
        with db.get_cursor() as cursor:
            cursor.execute('''SELECT user_id, username, role, status
                        FROM users ORDER by user_id;''')
            all_users = cursor.fetchall()
            return render_template('all_users.html', all_users=all_users)
    else: 
        return render_template('access_denied.html'),403


#individual user details, update status and role
@app.route('/manage_users', methods=['GET','POST'])
@login_required()
def manage_users():
    login_role=session.get('role')
    user_id=request.args.get('id')
    if login_role !="admin":
        return render_template('access_denied.html'),403
# display the user info based
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT user_id,username, email,first_name,
                        last_name, location, profile_image,
                        role, status FROM users 
                        WHERE user_id=%s;''',(user_id,))
        manage_user= cursor.fetchone()
# update user status /role (admin only)
    if request.method=='POST':
        user_id= request.form.get('id')
        user_role=request.form.get('user_role')
        status=request.form.get('status')
        with db.get_cursor() as cursor:
            cursor.execute('''UPDATE users SET role =%s,
                            status= %s WHERE user_id=%s''',(user_role,status,user_id,))
            flash('User profile has been updated','success')
#display the updated info once successful
            cursor.execute('''SELECT user_id,username, email,first_name,
                            last_name, location, profile_image,
                            role, status FROM users 
                            WHERE user_id=%s;''',(user_id,))
            manage_user= cursor.fetchone()
    return render_template('manage_user.html', manage_user=manage_user)


# logout route
@app.route('/logout')
@login_required()
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('Successfully logged out! See you soon.', 'success')
    return redirect(url_for('home_page'))
