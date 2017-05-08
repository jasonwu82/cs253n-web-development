

import webapp2
import cgi
import string
form = """
Please enter text for rot13 converting:
<br>
<form id="textform" method="post">
    <textarea rows="4" cols="50" name="text" form="textform">%(text)s</textarea>
    <input type="submit">
</form>
<br>

"""
text=""
def convert_rot13(str):
    new_s_list = []
    for c in str:
        if c in string.ascii_lowercase:
            order = (ord(c)-ord('a')+13)%26
            new_s_list += chr(ord('a') + order)
        elif c in string.ascii_uppercase:
            order = (ord(c)-ord('A')+13)%26
            new_s_list += chr(ord('A') + order)
        else:
            new_s_list += c
    new_s = ''.join(new_s_list)
    new_s = cgi.escape(new_s,quote=True)
            
    return new_s

class Rot13_handler(webapp2.RequestHandler):
    def get(self):
        
        self.response.write(form % {"text":"text to convert..."})
    def post(self):
        text = self.request.get("text")
        self.response.write(form % {"text":convert_rot13(text)})