# models.py

from google.appengine.ext import db
from pygooglechart import SparkLineChart

class Reporter( db.Model ):
    name = db.StringProperty()
    added_on = db.DateTimeProperty(auto_now_add=True)

    def spark_line_url( self, challenge ):
        sl = SparkLineChart( 160, 10 )
        data = [ report.score() for report in challenge.report_set.filter( 'reporter = ', self ).order("reported_date") ]
        sl.add_data( data )
        return sl.get_url()
    
class Challenge( db.Model ):
    name = db.StringProperty()
    start = db.DateProperty()

    def top_reporters( self ):
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
        return sorted_scores

class Report( db.Model ):
    reporter = db.ReferenceProperty(Reporter)
    challenge = db.ReferenceProperty(Challenge)
    reported_date = db.DateProperty()
    flights_up = db.IntegerProperty()
    flights_down = db.IntegerProperty()

    def score( self ):
        return self.flights_up + int( .5 * self.flights_down )

