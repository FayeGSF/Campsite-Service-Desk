# Getting started
<p>On the landing page, users can login or register as new user. <br>
Use any of the available user IDs that have been created ( 3 admin, 5 helpers and 21 visitors ) in:  <br><em>password_hash_generator.py</em> to log in or register as new user.<br></p>

6 users have preloaded profile image as indicated in the appendix.

<p>When registering a user, username must be unique and password must contain 1 special character and 1 numeric character. </p>

## Homepage / user dashboard
Once logged in:
<p>Depending on the user role, the homepage will display the links applicable to their role access.<br>
<strong>Visitors</strong> : Edit profile, update password, view issues <br>
<strong>Helpers</strong> : Visitor links + view resolved issues <br>
<strong>Admin</strong>: Visitor links + view resolved issues, view users</p>

<p> "Home" and "LCC Issue Tracker" directs the user back to the user homepage / dashboard.</p>

In the user hompage/dashboard and navbar, there are links to perform actions like:<br>
### 1. Edit Profile 
    - All registered new users can upload or remove their profile picture in "View Profile"
    - Remove profile picture by clicking on the remove profile button. 
    - Change their first and last name, email, location.
    - Username can not be changed. However, users can recreate a new account with the same personal
        details (first and last name, email and country) under a different username.
    - Only admin can change a user's role and user status in "View Users".
### 2. Update Password
    - User will have to enter their current password and confirm it
    - Enter new password based on the guide (eg. contain 1 number and special character).
    - Errors will be triggered under certain conditions (eg. new password is the same as current password).

### 3. View Issues
    - As per requirements, visitors may view issues that they raised.
    - The search bar performs a blanket search across the issue tables and is case insensitve.
    - Only "New, Open and Stalled" issues are displayed. 
    - Resolved issues are available to admin and helpers only.
#### Issue Details
    - Issue details can be viewed by clicking on issue id number. 
    - All user roles can add comments in the issue details by clicking on the issue id and clicking on 
        the 'Add comment' button.
    - Admin and helpers can change the status of the issue via the issue details and 
        clicking the the update issue button. Depending on the exisiting status (new, stalled, resolved), 
        adding a comment will automatically change the issue status to 'open'.
    - A success alert will flash when either a comment or status update has been performed successfully. 
    
    Note: Updating issue status and adding a comment cannot be performed simultaneously.
    eg. Setting issue to resolved with a comment, first add the comment, followed by updating issue status. 
### 4. Report an Issue
    - The link is in the navbar. 
    - Visitors will have the default issue status -'new', admin and helpers select any appropriate status. 
    - All text fields must be filled before the issue can be submitted.
    - A success alert will flash when the issue has been reported successfully. 
<p> The "logout" button will redirect the user to the login page if they are not logged in.</p>

### 5. View Resolved Issues 
    - This is accessible to both admin and helpers. 
    - However, only admin can click on the user_id which redirects them to the user detail page . 
    - As per the search bar in view issues, it is a blanket search bar that is case insensitive.
    - Admin and helpers can click on the issue id to view the details and add comments. This will 
        trigger the issue status to 'open' and return to the issue to the 'View Issues' table.

### 6. View users (admin only)
    - Admin users are able to modify the role and status of each user, including themselves. 
    - If admin changes their own status or role, the role access changes will only be effective the next time
        they are logged in. 
    -Inactive users will not be able to log in, they will be redirect to the log in page. 
### 7. Logout
    - Logging out successfully will be confirmed with a flash message. 
    
## References:
<li><strong>Default user picture:</strong> <br> https://www.shutterstock.com/image-vector/user-profile-icon-vector-avatar-person-2220431045"/li>
<li><strong>User_8 profile picture:</strong><br>https://www.freepik.com/free-photo/front-view-beautiful-young-woman_6882342.htm#fromView=keyword&page=2&position=42&uuid=0e7e86d5-326a-4dfb-90ee-0b47ae7178ea&query=Headshot+Portrait</li>
<li><strong>User_18 profile picture:</strong><br> https://www.freepik.com/free-photo/closeup-young-female-professional-making-eye-contact-against-colored-background_27507695.htm#fromView=keyword&page=1&position=1&uuid=0aa65765-2ffa-4d93-afde-872e889654c2&query=Headshot+Profile</li>
<li><strong>User_21 profile picture:</strong><br> https://www.freepik.com/free-photo/tourist-by-bonfire-forest_2527751.htm#fromView=search&page=1&position=25&uuid=7a4b70d7-66d8-48fc-bb55-49b86164187b&query=camp+profile+picture</li>
<li><strong>User_3 profile picture: </strong><br>https://www.freepik.com/free-photo/close-up-man-with-headphones_11094473.htm#fromView=search&page=1&position=35&uuid=7a4b70d7-66d8-48fc-bb55-49b86164187b&query=camp+profile+picture</li>
<li><strong>User_28 profile picture: </strong><br>https://www.shutterstock.com/image-photo/close-headshot-portrait-picture-smiling-african-1733598437
<li><strong>User_29 profile picture:</strong><br>
https://cointelegraph.com/crypto-betting/author/juliencovillaud/</li>
<li><strong>Homepage background:</strong><br>https://thecamp.co.nz/

### Appendix

Below are the users with pre-loaded profile picture:

User_id: 3 , Username: 'robertobrowno' <br>
User_id: 8 , Username: 'LinDavis'<br>
User_id: 18 , Username: 'Nancy24wRight' <br>
User_id: 21 , Username: 'Danieldaygreen' <br>
User_id: 28 , Username: 'LisaRoberts'<br>
User_id: 29 , Username: 'briAnwalkErr<br>
