# The entry point to the webapp
# API import 
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

#local imports
from handlers import MainPage, Register, WebRegister, Event, ListVisitors, WebVisitors

application = webapp.WSGIApplication(
  [('/', MainPage), 
   ('/register', Register),
   ('/webregister',WebRegister),
   ('/admin', ListVisitors),
    ('/admin/web', WebVisitors),
   ('/event/create', Event)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
