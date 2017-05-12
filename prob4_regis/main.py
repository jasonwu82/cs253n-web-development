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

import webapp2
import signup
import login
form="""
This is Hungwei's main page
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup',signup.Signup_handler),
    ('/signup/welcome',signup.Welcome_handler),
    ('/login',login.Login_handler),
    ('/logout',signup.Logout_handler)
], debug=True)

