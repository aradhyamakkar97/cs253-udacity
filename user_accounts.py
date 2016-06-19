# user accounts from scratch
import jinja2
import webapp2
from google.appengine.ext import db
import re
import hashlib
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'),autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

dict_of_users={}

def makeCookieValue(u,p):
    return u+'|'+hashlib.sha256(p).hexdigest()

def checkCookie(c):
    if c:

        username=''
        for i in c:
            if i=='|':
                break
            else:
                username+=i
        password=dict_of_users.get(username)
        if password:
            if c==makeCookieValue(username,password):
                return True
            else:
                return False
        else:
            return False
    else:
        return False




class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class MainPage(Handler):
    def get(self):
        self.write('bullshit')


class SignUp(Handler):

    def get(self):
        c=self.request.cookies.get('user_id')
        if c!='' and checkCookie(c) :
            self.redirect('./welcome')
        else:
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
        if username in dict_of_users.keys():
            everythingCorrect=False

        if not everythingCorrect:
            self.render('signup.html',username=username,email=email,error='daal mei kuch kaala hai')
        else:
            dict_of_users[username]=password
            v = makeCookieValue(username,password)

            self.response.headers.add_header('Set-Cookie', str('user_id='+v+'; Path=/'))
            self.redirect('/welcome')


class Welcome(Handler):
    def get(self):
        c=self.request.cookies.get('user_id')
        if c!='' and checkCookie(c) :
            username=''
            for i in c:
                if i=='|':
                    break
                else:
                    username+=i
            self.write('welcome '+username)
        else:
            self.redirect('/signup')

class Login(Handler):
    def get(self):
        c=self.request.cookies.get('user_id')
        if c!='' and checkCookie(c) :
            self.redirect('/welcome')
        else:
            self.render('login.html')
    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')

        try:
            if dict_of_users[username]==password:
                v = makeCookieValue(username,password)
                self.response.headers.add_header('Set-Cookie', 'user_id='+v+'; Path=/')
                self.redirect('/welcome')
            else:
                self.render('login.html',error='password is incorrect')
        except:
            self.render('login.html',error='username doesnt exist')




class Logout(Handler):
    # redirects to signup page and clears any cookies. MEans LOGS me out
    def get(self):
        #log the fuck out ( clear the fking cookies ) and then :
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/signup')



app=webapp2.WSGIApplication( [('/',MainPage),('/signup',SignUp),('/welcome',Welcome),('/login',Login),
('/logout',Logout)] ,debug=True )
