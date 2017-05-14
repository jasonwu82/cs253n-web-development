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
from google.appengine.api import memcache
import blog_db
import json
import logging
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
POSTS = "posts"
query_time = time.time()
class BlogPage_handler(webapp2.RequestHandler):
    def get(self):
        global query_time
        posts = memcache.get(POSTS)
        if posts is None:
            # read DB
            logging.info("DB query")
            query_time = time.time()
            posts = blog_db.Post.query().fetch()
            memcache.set(POSTS,posts)
        
        template = JINJA_ENVIRONMENT.get_template("blog.html")
        query_interval = time.time() - query_time
        self.response.write(template.render(posts=posts,query_interval="%.1f" % query_interval))

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
        # clear memcache
        memcache.delete(POSTS)
        
        #add new post and query time to single post memcache
        if not memcache.add(str(newpost.key.id), (newpost,time.time())):
            logging.error("id already exist for new post")
        self.redirect('/blog/'+str(newpost.key.id()))

class Post_id_handler(webapp2.RequestHandler):
    def get(self,post_id):
        #post = blog_db.Post.get_by_id(int(post_id))
        # get single post and query time
        singlepost_cached = memcache.get(post_id)
        prev_qeury_time = None
        post = None
        if not singlepost_cached:
            logging.info("get single post with DB query")
            post = blog_db.Post.get_by_id(int(post_id))
            prev_qeury_time = time.time()
            memcache.set(post_id,(post,prev_qeury_time))
        else:
            post, prev_qeury_time = singlepost_cached
        template = JINJA_ENVIRONMENT.get_template("single_post.html")
        if not post:
            self.response.write(template.render(error="Can't find the post with this id!"))
            return
        self.response.write(template.render(subject=post.subject,
            content=post.content,query_interval="%.1f" % (time.time()-prev_qeury_time)))
    
class Post_id_json_handler(webapp2.RequestHandler):
    def get(self,post_str):
        post_id = post_str.split(".")[0]
        post = blog_db.Post.get_by_id(int(post_id))
        post = post.to_dict()
        if post and post.get("created"):
            post["created"] = str(post["created"])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(post))
        
class Flush_handler(webapp2.RequestHandler):
    def get(self):  
        memcache.flush_all()
        self.redirect('/blog')
    
    
    

