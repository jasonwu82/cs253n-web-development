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
import blog
import signup
import login
import wiki
import json
form="""
This is Hungwei's main page
"""
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("index.html")
        template_values = {}
        self.response.write(template.render(template_values))
class Main_page_json(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write("")

main_url_mapping = [
    ('/', MainPage),
    ('/.json',blog.BlogPage_json_handler), 
]
blog_url_mapping = [(r'/blog/?',blog.BlogPage_handler),
    (r'/blog/?.json',blog.BlogPage_json_handler),
    ('/blog/newpost',blog.Newpost_handler),
    (r'/blog/(\d+)', blog.Post_id_handler),
    (r'/blog/(\d+).json', blog.Post_id_json_handler),
    ('/blog/signup',signup.Signup_handler),
    ('/blog/signup/welcome',signup.Welcome_handler),
    ('/blog/login',login.Login_handler),
    ('/blog/logout',signup.Logout_handler),
    ('/blog/flush',blog.Flush_handler)
    ]
    
wiki_url_mapping = [
    
    ('/wiki/signup',signup.Signup_handler),
    ('/wiki/signup/welcome',signup.Welcome_handler),
    ('/wiki/login',login.Login_handler),
    ('/wiki/logout',signup.Logout_handler),
    ('/wiki/flush',blog.Flush_handler),
    (r'/wiki/_edit/?\w*',wiki.WikiPage_edit_handler),
    (r'/wiki/?\w*',wiki.WikiPage_handler),
]
all_url_mapping = main_url_mapping + blog_url_mapping + wiki_url_mapping
app = webapp2.WSGIApplication(all_url_mapping, debug=True)

