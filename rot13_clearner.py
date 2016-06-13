import webapp2
import cgi
import string
form = ''' <html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
'''

def rot13(text):
    l=list(string.ascii_lowercase)

    new=[]
    for i in text:
        if i.lower() in l:
            if i.islower():
                new.append(l[(l.index(i)+13)%26].lower())
            else:
                new.append(l[(l.index(i.lower())+13)%26].upper())
        else:
            new.append(i)
    return ''.join(new)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form %'')
    def post(self):
        self.response.write(form % cgi.escape(rot13(self.request.get("text"))))


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
