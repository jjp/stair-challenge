# views.py
import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list, object_detail

from ragendja.dbutils import transaction

from challenge.models import Reporter, Challenge, Report
from challenge.forms import ChallengeForm, ActivityReportForm

def list_challenges(request):
    return object_list(request, Challenge.all(), paginate_by=10)

def main( request ):
    return render_to_response(
        'main.html', {} )

def add_challenge( request ):
    result = ""
    if( request.method == 'POST' ):
        form = ChallengeForm( request.POST )
        if( form.is_valid() ):
            challenge = Challenge()
            challenge.name = form.cleaned_data['name']
            challenge.put( )
            return HttpResponseRedirect(reverse('challenge.views.show_challenge', kwargs={'id':str(challenge.key().id() ) }) )
    else:
        # default to GET
        form = ChallengeForm( )
    
    return render_to_response('challenge/new_challenge.html', {'form': form } )

    return HttpResponse( result )

def show_challenge( request, id ):
    challenge = Challenge.get_by_id( int(id ) )
    
    if( request.method == 'POST' ):
        return _new_activity_report( request, challenge )
    else:
        form = ActivityReportForm(
            initial = { 'challenge_id': id } )
        reports = challenge.report_set.order("-reported_date")
        top_reporters = challenge.top_reporters( )[0:3]
        return object_list(request, reports, paginate_by=15, extra_context=locals(), template_name='challenge/activity_report.html' )
        # return render_to_response( 'challenge/activity_report.html', locals() )

def spark_line( request, challenge_id, reporter_id ):
    challenge = Challenge.get_by_id( int( challenge_id ) )
    reporter = Reporter.get_by_id( int( reporter_id ) )
    return HttpResponseRedirect(reporter.spark_line_url( challenge ) )

def admin( request ):
    return HttpResponse( 'admin' )

def _new_activity_report( request, challenge ):
    # first get list of existing reporters for dropdown
    form = ActivityReportForm( request.POST )
    if( form.is_valid() ):
        name = form.cleaned_data['reporter_new_name'] or form.cleaned_data['reporter_existing_name']
        query =  Reporter.all()
        query.filter('name =', name )
        results = query.fetch(1)
        if( len( results ) ):
            reporter = results[0]
        else:
            reporter = Reporter( name = name )
            reporter.put( )
        report = Report( reporter = reporter, challenge = challenge,
                         reported_date = _makeDate( form.cleaned_data['reported_date'] ),
                         flights_up = form.cleaned_data['flights_up'],
                         flights_down = form.cleaned_data['flights_down'] )
        report.put()
        return HttpResponseRedirect(reverse('challenge.views.show_challenge', kwargs={'id':str(challenge.key().id() ) }) )
    else:
        reports = challenge.report_set
        return render_to_response( 'challenge/activity_report.html', locals() )

def _makeDate( friendly_date ):
    return datetime.datetime.strptime( friendly_date, "%Y-%m-%d" ).date()
    # should be yesterday or today
    today = datetime.date.today()
    if( friendly_date == 'today' ):
        selected_date = today
    elif( friendly_date == 'yesterday' ):
        selected_date = today - datetime.timedelta( days = 1 )
    else:
        # let's try and make a sensible date
        selected_date = datetime.datetime.strptime( friendly_date, "%Y-%m-%d" )
        
    return selected_date
