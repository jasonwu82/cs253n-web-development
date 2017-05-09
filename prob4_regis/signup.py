

import webapp2
import cgi
import string
import re
import os
import jinja2

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
            self.response.set_cookie('username', signup_text['username'],path='/')
            self.redirect('/signup/welcome')
        else:
            form_dict = signup_text.copy()
            form_dict.update(error_text)
            template = JINJA_ENVIRONMENT.get_template("signup.html")
            template_values = form_dict
            self.response.write(template.render(template_values))
            
        
class Welcome_handler(webapp2.RequestHandler):        
    welcome_form="Welcome, %(username)s !"
    def get(self):
        username = self.request.cookies.get('username')
        self.response.write(self.welcome_form % {"username":username})
        
        
        
        
        