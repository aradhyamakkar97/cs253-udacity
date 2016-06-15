import os
import jinja2
import webapp2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'),autoescape=True)

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
        self.write('meow')



app=webapp2.WSGIApplication( [('/',MainPage),] ,debug=True )
