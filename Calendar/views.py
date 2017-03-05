from django.shortcuts import render

# Create your views here.
def index(request, calendar_slug):
    try:
        schedule = schedule.objects.get(pk=schedule)
    except Question.DoesNotExist:
        raise Http404("The requested calendar does not exist")
    return render(request, 'schedule/calendar.html', {'calendar_slug': calendar_slug})