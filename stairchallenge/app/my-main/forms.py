from django import forms
from stairchallenge.main.models import Reporter
import datetime

MONTHS = (
    (1, 'January' ),
    (2, 'Feburary' ),
    (3, 'March' ),
    (4, 'April' ),
    (5, 'May' ),
    (6, 'June' ),
    (7, 'July' ),
    (8, 'August' ),
    (9, 'September' ),
    (10, 'October' ),
    (11, 'November' ),
    (12, 'December' ),
)

today = datetime.date.today()
day = datetime.timedelta( days = 1 )
yesterday = today - day
DATES = (
    ( today.isoformat(), 'Today' ),
    ( yesterday.isoformat(), 'Yesterday' ),
)
day_range = range( 2, 7 )
dates = [ today - (i * day) for i in day_range ]

DATES = DATES + tuple([ (d.isoformat(), "%d days ago (%s)" % ( i, d.strftime( "%A" ) ) ) for i, d in zip( day_range, dates ) ])

class ChallengeForm( forms.Form ):
    name = forms.CharField()
    start_month = forms.ChoiceField( choices = MONTHS )

class ActivityReportForm( forms.Form ):

    def __init__(self, *args, **kwargs):
        super(ActivityReportForm, self).__init__(*args, **kwargs)
        self.fields['reporter_existing_name'].choices = [
            ('', "--------" ) ] + [
            ( reporter.name, reporter.name ) for reporter in Reporter.all()
            ]
    
    challenge_id = forms.IntegerField(widget = forms.HiddenInput)
    reporter_new_name = forms.CharField( required = False )
    reporter_existing_name = forms.ChoiceField( choices=(()), required=False )
    reported_date = forms.ChoiceField( choices = DATES )
    flights_up = forms.IntegerField()
    flights_down = forms.IntegerField()


    
