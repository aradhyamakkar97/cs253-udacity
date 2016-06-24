import jinja2
import webapp2
from google.appengine.ext import db
from google.appengine.api import memcache # not gonna use it, will just use a dictionary for caching
import time
import logging


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'),autoescape=True)

updated=True
CACHE = {}
var=0
start = 0




class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class FlushHandler(Handler):
    def get(self):
        CACHE.clear()
        self.redirect('/')

class MainPage(Handler):
    def get(self):
        global updated,var,start


        key = 'front'
        if (key in CACHE) and  updated==True:
            posts = CACHE[key]
            var = time.time()-start

        else:
            logging.error('fuck')
            posts= db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
            posts=list(posts)
            CACHE[key]=posts
            updated = True
            var = 0
            start= time.time()


        self.render('frontpage.html', posts=posts,var=var)

class NewPost(Handler):
    def get(self):
        self.render('form.html')
    def post(self):
        global updated
        subject=self.request.get('subject')
        content=self.request.get('content')

        if subject and content :
            a=Blog(subject=subject,content=content)
            a.put()
            updated = False
            idd=a.key().id()
            # now i have to go to permanent link where i will display a.
            self.redirect('/'+str(idd))


        else:
            self.render('form.html',error='need both subject and content',subject=subject,content=content)

class DynamicHandler(Handler):
    def get(self,me):
        # need to get object from url, which contains id of the object and name that object a
        key = str(me)
        if key in CACHE:
            a= CACHE[key][0]
            CACHE[key][1]=time.time()- CACHE[key][2]
        else:

            a=Blog.get_by_id(int(me))
            logging.error('fucked :-  doing a db query')
            if a!=None:
                CACHE[key]=[a,0,time.time()]
        if a:
            s=CACHE[key][1]
            self.render('perm.html',post=a,s=s)
        else:
            self.write('no entry for this id')


app=webapp2.WSGIApplication( [('/',MainPage),('/newpost',NewPost),(r'/(\d+)', DynamicHandler),('/flush',FlushHandler)] ,debug=True)
