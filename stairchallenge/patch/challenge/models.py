# models.py

from google.appengine.ext import db


class Reporter( db.Model ):
    name = db.StringProperty()
    added_on = db.DateTimeProperty(auto_now_add=True)

class Challenge( db.Model ):
    name = db.StringProperty()
    start = db.DateProperty()

    def top_reporters( self, limit=5 ):
        all_reporters = Reporter.all( )
        scores = []
        for reporter in all_reporters:
            reports = self.report_set
            reports.filter( 'reporter = ', reporter )
            score = 0
            for reporter_reports in reports:
                score = score + reporter_reports.flights_up + (.5 * reporter_reports.flights_down )
            scores.append( ( reporter, int(score) ) )
        sorted_scores = sorted( scores, lambda x, y: x[1] - y[1], reverse=True )
        return sorted_scores[0:limit]

class Report( db.Model ):
    reporter = db.ReferenceProperty(Reporter)
    challenge = db.ReferenceProperty(Challenge)
    reported_date = db.DateProperty()
    flights_up = db.IntegerProperty()
    flights_down = db.IntegerProperty()

