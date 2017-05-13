import webapp2
import jinja2
import os
import db_users
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
error_msg = "invalid username or password"   

class Login_handler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("login.html")
        self.response.write(template.render({}))
        
    def post(self):
        template = JINJA_ENVIRONMENT.get_template("login.html")
        username = self.request.get("username")
        password = self.request.get("password")
        if not username or not password:
            error = error_msg
            self.response.write(template.render(error=error))
            return
        oldUsers = db_users.User.query(db_users.User.username.IN([username])).fetch()
        
        # here, only retrieve the first user (assume no multiple entity with same username)
        # need to assign username to private key?
        if not oldUsers or oldUsers[0].password != password:
            error = error_msg
            self.response.write(template.render(error=error))
            return
        self.response.set_cookie('username', username,path='/')
        self.redirect('/signup/welcome')
        
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)