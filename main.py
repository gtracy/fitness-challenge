#!/usr/bin/env python

import os
import logging

from google.appengine.api import images
from google.appengine.api.taskqueue import Task
from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from dataModel import *


class MainHandler(webapp.RequestHandler):
    def get(self):
    
      # add the counter to the template values
      template_values = {'greeting':'',
                        }
      
      # generate the html
      path = os.path.join(os.path.dirname(__file__), 'templates/splash.html')
      self.response.out.write(template.render(path, template_values))

## end MainHandler

class CronHandler(webapp.RequestHandler):
    def get(self,period):
      self.post(period)
      return 'done'

    def post(self,period):
      logging.debug('looking for achievements to analyze...')
      # Get the list of active Achievement models for the respective time period ID
      awards = db.GqlQuery('select * from Achievement where time_period=:1',period).fetch(100)
      # Get the list of active Users
      users = db.GqlQuery('select * from User where active=True').fetch(100)

      for a in awards:
        logging.debug('check users for achievement %s' % a.name)
        for u in users:
          # check if the achievement has not been awarded for user
          logging.debug('does %s already have achievement %s?' % (u.name,a.name))
          if a.key() not in u.achievements:
            logging.debug('creating analysis task for %s' % a.name)
            # spawn a task for the user/achievement tuple
            task = Task(url='/achievements/analyze', 
                        params={'user':u.key(),
                                'award':a.key(),
                               })
            task.add('analyze')
    
      
## end CronHandler

class CreateUserHandler(webapp.RequestHandler):
    def post(self):
      u = User()
      u.name = self.request.get('name')
      u.phone_number = self.request.get('phone')
      u.active = True
      u.phone_notifications = True
      u.put()
      self.redirect('/achievements/new')

## end CreateUserHandler

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/cron/start/(.*)', CronHandler),
                                          ('/user/create', CreateUserHandler),
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
