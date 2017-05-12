

import webapp2
import cgi
import string
import re
import os
import jinja2
import db_users

signup_text = {"username":"","password":"","verify":"","email":""}
error_text = {"error_usr":"","error_password":"","error_verify_password":"","error_email":""}
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def valid_username(str):  
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(str)
    
def valid_password(str):  
    RE = re.compile(r"^.{3,20}$")
    return RE.match(str)
    
def valid_verify_password(ps1,ps2):
    return ps1==ps2
    
def valid_email(str):
    if str=="":
        return True
    RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return RE.match(str)
def verify_signup(signup_text):
    isValid = True
    if valid_username(signup_text["username"]):
        error_text["error_usr"] = ""
    else:
        error_text["error_usr"] = "This is an invalid username"
        isValid = False
    if valid_password(signup_text["password"]):
        error_text["error_password"] = ""
    else:
        error_text["error_password"] = "This is an invalid password"
        isValid = False
    if valid_verify_password(signup_text["password"],signup_text["verify"]):
        error_text["error_verify_password"] = ""
    else:
        error_text["error_verify_password"] = "Two password don't match" 
        isValid = False
    if valid_email(signup_text["email"]):
        error_text["error_email"] = ""
    else:
        error_text["error_email"] = "This is an invalid email"
        isValid = False
    return isValid
    

class Signup_handler(webapp2.RequestHandler):
    def get(self):
        form_dict = signup_text.copy()
        form_dict.update(error_text)
        
        template = JINJA_ENVIRONMENT.get_template("signup.html")
        template_values = form_dict
        self.response.write(template.render(template_values))
        
    def post(self):
        signup_text = dict(self.request.POST.items())
        isValid = verify_signup(signup_text)
        if isValid:
            # store password in clear text currently
            
            
            # check if exist
            # delete all old same username (overwrite)
            oldUsers = db_users.User.query(db_users.User.username.IN([signup_text["username"]])).fetch()
            for u in oldUsers:
                u.key.delete()
            newUser = db_users.User(username=signup_text["username"],password=signup_text["password"])
            newUser.put()
            
            self.response.set_cookie('username', signup_text['username'],path='/')
            self.response.set_cookie('token', db_users.user_encrypt_token(signup_text['username']),path='/')
            self.redirect('/blog/signup/welcome')
        else:
            form_dict = signup_text.copy()
            form_dict.update(error_text)
            template = JINJA_ENVIRONMENT.get_template("signup.html")
            template_values = form_dict
            self.response.write(template.render(template_values))
            
        
class Welcome_handler(webapp2.RequestHandler):        
    
    def get(self):
        # no handle for non-exist user
        username = self.request.cookies.get('username')
        token = self.request.cookies.get('token')
        template = JINJA_ENVIRONMENT.get_template("welcome.html")
        if not username:
            self.redirect('/blog/signup')
            print('not username')
            return
        #user = db_users.User.query(db_users.User.username.IN([signup_text["username"]])).fetch()
        # check if user is in database
        if not token:
            print(token)
            print("not user or not token")
            self.redirect('/blog/signup')
            return
        if not db_users.verify_token(username, token):
            print('not verify token')
            self.redirect('/blog/signup')
            return
        self.response.write(template.render(username=username))
        
class Logout_handler(webapp2.RequestHandler):
    def get(self):
        self.response.set_cookie('token', "",path='/')
        self.redirect('/blog/signup')
        
        
        
        
        