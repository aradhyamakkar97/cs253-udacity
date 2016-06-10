import webapp2
import cgi
form = """

<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(val)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""
def rot13(someString):
    arr=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
    'v','w','x','y','z']

    toReturn=[]

    for i in someString:
        if i.lower() in arr:
            for j in range(len(arr)):
                if (arr[j]==i.lower()):
                    break
            if (i.islower()):
                toReturn.append(arr[(j+13)%26])
            else:
                toReturn.append(arr[(j+13)%26].upper())
        else:
            toReturn.append(i)

    return ''.join(toReturn)





class MainHandler(webapp2.RequestHandler):

    def write_form(self,value=""):
        self.response.write(form % {"val":value})

    def get(self):
        self.write_form()

    def post(self):
        a = self.request.get("text")
        #a=cgi.escape(a)
        b= rot13(a)
        b=cgi.escape(b)
        self.write_form(b)


app = webapp2.WSGIApplication([('/', MainHandler)],debug=True)
