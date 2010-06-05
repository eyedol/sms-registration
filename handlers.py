import os
from google.appengine.api import users
from google.appengine.ext import webapp
from sms_message import IncomingSMSMessage
from web_registeration import Registration
from google.appengine.ext.webapp import template
from models import db

'api key to get legitimate content. dummy for now'
API_KEY = 'XYZ'
class MainPage(webapp.RequestHandler):
    """
    This is a debugging page that allows me to test how the code handles messages.
    """
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/web_registration.html')
        self.response.out.write(template.render(path, template_values))

class WebRegister(webapp.RequestHandler):
    
    debug = False
    
    #def get(self):
     #   self.post()

    def post(self):
        reg = Registration( self.request.get('fname'),self.request.get('email'),
        self.request.get('expectation'))
        confirmation = reg.confirm()
        event = reg.save()

        if reg:
            template_values = {'event': event,'confirmation':confirmation}
            path = os.path.join(os.path.dirname(__file__),'templates/notification.html')
            self.response.out.write(template.render(path, template_values))


class Register(webapp.RequestHandler):
    'Handles the form submission'
    debug = False
    
    """def get(self):
        'Pass on get requests to the post handler.'
        self.post()"""

    def post(self):
	'Handle the post request.'
        api_key = self.request.get('api_key')

        'hope its not a spammer'
        if len(api_key) > 0 and api_key == API_KEY:
	    msg = IncomingSMSMessage(self.request.get('phone'), 
	    self.request.get('body'))
	    msg.confirm()
	    event = msg.save()

        if msg:
            template_values = {'event': event}
	    path = os.path.join(os.path.dirname(__file__), 'templates/notification.html')
	    self.response.out.write(template.render(path, template_values))

class ListVisitors(webapp.RequestHandler):
    """
        This is a debugging page that allows me to test how the code creates events."""

    def get(self):
        
        """ This page only shows if a user is an admin """
        
        if users.is_current_user_admin():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            weburl = 'admin/web'
            weburl_linktext = 'Web List'

            """ Lets fetch everything for now and figure out 
            pagination later. """

            visitors = db.GqlQuery("SELECT * FROM RegisteredVisitor ORDER BY phone DESC ")
        
            template_values = {
                    'visitors': visitors,
                    'url':url,
                    'url_linktext':url_linktext,
                    'weburl':weburl,
                    'weburl_linktext':weburl_linktext
                    }

            path = os.path.join(os.path.dirname(__file__), 
                    'templates/admin/visitor_list.html')
	    self.response.out.write(template.render(path, template_values))

        else:
            self.redirect(users.create_login_url(self.request.uri))

class WebVisitors(webapp.RequestHandler):
    """
        This is a debugging page that allows me to test how the code creates events."""

    def get(self):
        
        """ This page only shows if a user is an admin """
        
        if users.is_current_user_admin():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            
            smsurl = '/admin'
            smsurl_linktext = 'SMS List'

            """ Lets fetch everything for now and figure out 
            pagination later. """

            visitors = db.GqlQuery("SELECT * FROM WebRegistered ORDER BY phone DESC ")
        
            template_values = {
                    'visitors': visitors,
                    'url':url,
                    'url_linktext':url_linktext,
                    'smsurl':smsurl,
                    'smsurl_linktext':smsurl_linktext
                    }

            path = os.path.join(os.path.dirname(__file__), 
                    'templates/admin/web_visitor_list.html')
	    self.response.out.write(template.render(path, template_values))

        else:
            self.redirect(users.create_login_url(self.request.uri))



class Event(webapp.RequestHandler):
    """
    This is a debugging page that allows me to test how the code creates events.
    """
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/event.html')
        self.response.out.write(template.render(path, template_values))

