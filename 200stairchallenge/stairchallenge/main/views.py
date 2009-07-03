# views.py

from django.http import HttpResponse

from stairchallenge.main.models import Visitor

def main(request):
    visitor = Visitor()
    visitor.ip = request.META["REMOTE_ADDR"]
    visitor.put()

    result = "<pre>"
    visitors = Visitor.all()
    visitors.order("-added_on")

    for visitor in visitors.fetch(limit=40):
        result += visitor.ip + u" visited on " + unicode(visitor.added_on) + u"\n"

    result = result + "</pre>"
    return HttpResponse(result)


