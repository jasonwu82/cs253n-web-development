import os
import urllib
import webapp2

import jinja2
from google.appengine.ext import ndb
from google.appengine.api import memcache
import blog_db
import json
import logging
import time
import signup
import db_wiki
import re
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



def get_wiki_by_title(title):
    # return None if not found
    # no memcache now
    pass
class WikiPage_handler(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        logging.error("path is %s" % path)
        title = ""
        if re.match("/wiki/?",path):
            logging.error("match mainpage")
            title = ""
        wiki_page = db_wiki.get_wiki_page(title)    

        username = self.request.cookies.get('username')
        token = self.request.cookies.get('token')
        
        if not signup.isValidUserToken(username,token):
            # not logged in
            template = JINJA_ENVIRONMENT.get_template("wiki_not_login.html")
            content = "This is empty page"
            if wiki_page:
                content = wiki_page.content
            self.response.write(template.render(wiki_content_view=content))
            return
        # is logged in
        template = JINJA_ENVIRONMENT.get_template("wiki_logged_in_view.html")
        content = "This is empty page"
        if wiki_page:
            content = wiki_page.content
        edit_href = "/wiki/_edit/%s" % title
        self.response.write(template.render(wiki_title=title,wiki_content_view=content,edit_href=edit_href))

class WikiPage_edit_handler(webapp2.RequestHandler):
    def get(self):
        
        pass
        
        
        
        
        
        
        
        