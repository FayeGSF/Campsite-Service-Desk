from flask import Flask
app = Flask(__name__)

app.secret_key ="lcc_issues_trackerLincolnCOMP639"

# from lcc_issue_app import connect,db,home,auth,user
#import only if there are routes,set-up to define it 
import lcc_issue_app.connect as connect
import lcc_issue_app.db as db
import lcc_issue_app.home
import lcc_issue_app.auth
import lcc_issue_app.user 

# Initialize the database
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)
import sys
print(sys.path)