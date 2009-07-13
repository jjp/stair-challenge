# models.py

from google.appengine.ext import db


class Reporter( db.Model ):
    name = db.StringProperty()
    added_on = db.DateTimeProperty(auto_now_add=True)

class Challenge( db.Model ):
    name = db.StringProperty()
    start = db.DateProperty()

class Report( db.Model ):
    reporter = db.ReferenceProperty(Reporter)
    challenge = db.ReferenceProperty(Challenge)
    reported_date = db.DateProperty()
    flights_up = db.IntegerProperty()
    flights_down = db.IntegerProperty()
