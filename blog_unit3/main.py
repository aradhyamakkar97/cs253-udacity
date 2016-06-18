import jinja2
import webapp2
from google.appengine.ext import db

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'),autoescape=True)

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

class MainPage(Handler):
    def get(self):
        posts= db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render('frontpage.html', posts=posts)

class NewPost(Handler):
    def get(self):
        self.render('form.html')
    def post(self):
        subject=self.request.get('subject')
        content=self.request.get('content')

        if subject and content :
            a=Blog(subject=subject,content=content)
            a.put()
            idd=a.key().id()
            # now i have to go to permanent link where i will display a.
            self.redirect('/'+str(idd))


        else:
            self.render('form.html',error='need both subject and content',subject=subject,content=content)

class DynamicHandler(Handler):
    def get(self,me):
        # need to get object from url, which contains id of the object and name that object a
        a=Blog.get_by_id(int(me))
        if a:
            self.render('perm.html',post=a)
        else:
            self.write('no entry for this id')


app=webapp2.WSGIApplication( [('/',MainPage),('/newpost',NewPost),(r'/(\d+)', DynamicHandler)] ,debug=True)
