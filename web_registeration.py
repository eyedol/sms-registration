#import from sys
import hashlib
import urllib

#import from appengine
from google.appengine.api import urlfetch

# import from local 
from models import WebRegistered

# handles registration from the web
class WebRegistration(object):
	"""
	Represents an Registration
	"""

	def __init__(self):
	    'Constructor'
	    self.m_fname = None
	    self.m_email = None
            self.m_expectation = None
		
	def set_fname(self, fname):
	    'Accessor for first name'
	    self.m_fname = fname

	def set_email(self, email):
	    'Accessor for email address'
	    self.m_email = email

        def set_expectation(self, expectation):
            'Accessor for expectations'
            self.m_expectation = expectation
            
	def get_hash(self):
	    'Accessor for the hash'
	    if self.m_fname == None or self.m_email == None:
	        raise AttributeError
	    else:
		m = hashlib.sha1()
		data = "#".join((self.m_fname, self.m_expectation))
		m.update(data)
		return m.hexdigest()

	def confirm(self):
	    'Confirm receipt of the message. No default implementation.'
	    raise NotImplementedError

	def save(self):
	    'Save to the datastore'
	    user = WebRegistered()
	    user.fname = self.m_fname()
	    user.email = self.m_email()
            user.expectation = self.m_expectation()
	    user.hash = self.get_hash()
	    return user.put()

class Registration(WebRegistration):
	"""
	Respresents a registration from the web
	"""
	
        def __init__(self, fname, email,expectation):
            self.set_fname(fname)
            self.set_email(email)
	    self.set_expectation(expectation)

	def confirm(self):
	    'Use clickatell to confirm the message'
	    confirm_msg = "We are excited you are coming to Maker Faire Africa 2010, Aug 6-7. Your confirmation # is %s" % (self.get_confirmation_number())
	    
            return confirm_msg;

	def save(self):
	    'Override so that we can also write to google docs'
	    WebRegistration.save(self)

        def get_confirmation_number(self):
            'Return a digit number taken from the hash'
            hash = self.get_hash()
            subhash = ''
            if len(hash) > 11:
                subhash = hash[3:10]
            else:
                subhash = hash
            return subhash

