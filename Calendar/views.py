from django.shortcuts import render
from .forms import CalendarEventForm
# Create your views here.
def index(request, calendar_slug):
    try:
        schedule = schedule.objects.get(pk=schedule)
    except Question.DoesNotExist:
        raise Http404("The requested calendar does not exist")
    return render(request, 'schedule/calendar.html', {'calendar_slug': calendar_slug})

def new_appt(request):
    calform = CalendarEventForm()
    return render(request, 'calendarevents/new_appt.html', {'calform':calform })


def create(request):
    if request.method == 'POST':
        calform = CalendarEventForm(request.POST)
        if calform.is_valid():
            calform.save()
            return HttpResponse('Appointment Created!')
        else:
            return render(request, 'calendarevents/new_appt.html', {'calform':calform})
