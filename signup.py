import webapp2
import re
un=''
ps=''
vr=''
em=''
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(un)s">
          </td>
          <td class="error">
%(er_un)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(ps)s">
          </td>
          <td class="error">
%(er_ps)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(vr)s">
          </td>
          <td class="error">
%(er_vr)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(em)s">
          </td>
          <td class="error">
%(er_em)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

class MainHandler(webapp2.RequestHandler):


    def write_form(self,un='',er_un='',ps='',er_ps='',vr='',er_vr='',em='',er_em=''):
        self.response.write(form % {"un":un,"er_un":er_un,"ps":ps,"er_ps":er_ps,"vr":vr,"er_vr":er_vr,"em":em,"er_em":er_em})

    def get(self):
        self.write_form()

    def post(self):
        def everythingCorrect():
            global USER_RE,PASS_RE,EMAIL_RE,un,ps,vr,em



            un=self.request.get('username')
            ps=self.request.get('password')
            vr=self.request.get('verify')
            em=self.request.get('email')



            if ps==vr and USER_RE.match(un) and PASS_RE.match(ps) and (EMAIL_RE.match(em) or em==''):

                return True
            else:
                return False


        if everythingCorrect():

            self.redirect('/welcome') #(with username wala informtion ?)
        else:
            error_username_message=''
            error_verify_message=''
            error_password_message=''
            error_email_message=''

            if (not USER_RE.match(un)):
                error_username_message='username incorrect'
            if (not PASS_RE.match(ps)):
                error_password_message='incorrect password'
            if (ps!=vr):
                error_verify_message='passwords do not match'
            if (not EMAIL_RE.match(em)):
                error_email_message='incorrect email'
            if (em=='') :
                error_email_message=''
            self.write_form(un,error_username_message,'',error_password_message,'',error_verify_message,em,error_email_message)


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('welcome '+ un)
        #WRITE welcome page here with the username included


app = webapp2.WSGIApplication([('/', MainHandler),('/welcome',WelcomeHandler)],debug=True)
