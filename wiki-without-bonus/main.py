import jinja2
import webapp2
from google.appengine.ext import db # not gonna use it -  will just use variables
import hashlib
import re

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'),autoescape=True)

pages={}
accounts={'admin':'admin'}
logged_in=False

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class WikiPage(Handler):
    def get(self,me):
        if me in pages:
            self.render('wikipage.html',content=pages[me],edit_path='/_edit'+me)
        else:
            self.redirect('/_edit'+me)

class Signup(Handler):
    def get(self):
        self.render('signup.html')
    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        verify=self.request.get('verify')
        email=self.request.get('email')

        everythingCorrect=True

        if not USER_RE.match(username):
            everythingCorrect=False
        if not PASS_RE.match(password):
            everythingCorrect=False
        if password!=verify:
            everythingCorrect=False
        if username in accounts:
            everythingCorrect=False

        if not everythingCorrect:
            self.render('signup.html',username=username,email=email,error='daal mei kuch kaala hai')
        else:
            accounts[username]=password
            v = username+'|'+hashlib.sha256(password).hexdigest()
            self.response.headers.add_header('Set-Cookie', str('user_id='+v+'; Path=/'))
            self.write('a new account has been created and u are logged in from that account. now u can edit pages')


class Login(Handler):
    def get(self):
        # is cookie fkng tempered? 
        c=self.request.cookies.get('user_id')
        un=''
        if c !=None:
            for i in c:
                if i=='|':
                    break
                else:
                    un+=i
            if un in accounts:
                if un+'|'+hashlib.sha256(accounts[un]).hexdigest() == c :
                    logged_in=True
                else:
                    logged_in=False
            else:
                logged_in=False
        else:
            logged_in=False

        if logged_in:
            self.write('already logged in')
        else:
            self.render('login.html')
    def post(self):
        global logged_in
        username= self.request.get('username')
        password=self.request.get('password')

        if username not in accounts:
            self.render('login.html',error='invalid username')
        else:
            if accounts[username]!=password:
                self.render('login.html',error='invalid password')
            else:
                # now I am logged in!
                logged_in=True
                v = username+'|'+hashlib.sha256(password).hexdigest()
                self.response.headers.add_header('Set-Cookie', str('user_id='+v+'; Path=/'))
                self.write('now u r logged in, now u can edit pages')





class Logout(Handler):
    def get(self):
        global logged_in
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        logged_in=False
        self.write('you are not logged out')


class EditPage(Handler):
    def get(self,me):
        global logged_in
        # is cookie tampered?
        c=self.request.cookies.get('user_id')
        un=''
        if c !=None:
            for i in c:
                if i=='|':
                    break
                else:
                    un+=i
            if un in accounts:
                if un+'|'+hashlib.sha256(accounts[un]).hexdigest() == c :
                    logged_in=True
                else:
                    logged_in=False
            else:
                logged_in=False
        else:
            logged_in=False



        if logged_in:
            self.render('edit.html')
        else:
            self.write(r'u need to login first, go to /login')
    def post(self,me):
        stuff = self.request.get('stuff')
        pages[me]=stuff
        self.redirect(me)




PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               (PAGE_RE, WikiPage),
                               ],
                              debug=True)
