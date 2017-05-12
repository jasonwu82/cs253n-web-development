# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import urllib
import webapp2

import jinja2
from google.appengine.ext import ndb
import blog_db
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BlogPage_handler(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template("blog.html")
        posts = blog_db.Post.query().fetch()
        self.response.write(template.render(posts=posts))

# for blog mainpage json
class BlogPage_json_handler(webapp2.RequestHandler):
    def get(self):
        posts = [p.to_dict() for p in blog_db.Post.query().fetch()]
        for p in posts:
            if p.get("created"):
                p["created"] = str(p["created"])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(posts))
        
class Newpost_handler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("newpost.html")
        template_values = {}
        self.response.write(template.render(template_values))
    def post(self):
        template = JINJA_ENVIRONMENT.get_template("newpost.html")
        subject = self.request.get("subject")
        content = self.request.get("content")
        if not subject or not content:
            error = "Please submit correct form..."
            self.response.write(template.render(error=error))
            return
        # submit to database
        newpost = blog_db.Post(subject=subject,content=content)
        newpost.put()
        self.redirect('/blog/'+str(newpost.key.id()))

class Post_id_handler(webapp2.RequestHandler):
    def get(self,post_id):
        post = blog_db.Post.get_by_id(int(post_id))
        template = JINJA_ENVIRONMENT.get_template("single_post.html")
        if not post:
            self.response.write(template.render(error="Can't find the post with this id!"))
            return
        self.response.write(template.render(subject=post.subject,content=post.content))
    
class Post_id_json_handler(webapp2.RequestHandler):
    def get(self,post_str):
        post_id = post_str.split(".")[0]
        post = blog_db.Post.get_by_id(int(post_id))
        post = post.to_dict()
        if post and post.get("created"):
            post["created"] = str(post["created"])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(post))
        
    
    
    
    

