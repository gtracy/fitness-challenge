#!/usr/bin/env python

import os
import logging

from google.appengine.api import images
from google.appengine.api.taskqueue import Task
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from dataModel import *


class NewAchievementHandler(webapp.RequestHandler):
    def get(self):
    
      # add the counter to the template values
      template_values = {'greeting':'',
                        }
      
      # generate the html
      path = os.path.join(os.path.dirname(__file__), 'templates/award-new.html')
      self.response.out.write(template.render(path, template_values))

## end MainHandler

class CreateAchievementHandler(webapp.RequestHandler):
    def post(self):
      a = Achievement()
      a.name = self.request.get('name')
      a.description = self.request.get('desc')
      a.message = self.request.get('msg')
      a.time_period = self.request.get('period')
      a.put()
      self.redirect('/achievements/new')
      
## end CronHandler

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/achievements/new', NewAchievementHandler),
                                          ('/achievements/create', CreateAchievementHandler),
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
