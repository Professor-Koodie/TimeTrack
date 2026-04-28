import json

from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.db.models import Max
from .models import Timesheet
from django.views.generic import UpdateView, DeleteView
from .forms import NewTimesheetForm, TimesheetForm

MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

WEEK_TO_MONTH = {
    1: 1, 2: 1, 3: 1, 4: 1,
    5: 2, 6: 2, 7: 2, 8: 2,
    9: 3, 10: 3, 11: 3, 12: 3, 13: 3,
    14: 4, 15: 4, 16: 4, 17: 4,
    18: 5, 19: 5, 20: 5, 21: 5,
    22: 6, 23: 6, 24: 6, 25: 6, 26: 6,
    27: 7, 28: 7, 29: 7, 30: 7,
    31: 8, 32: 8, 33: 8, 34: 8, 35: 8,
    36: 9, 37: 9, 38: 9, 39: 9,
    40: 10, 41: 10, 42: 10, 43: 10, 44: 10,
    45: 11, 46: 11, 47: 11, 48: 11,
    49: 12, 50: 12, 51: 12, 52: 12, 53: 12, 54: 12,
}


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

@login_required(login_url='login')
def dashboard_view(request):
    form = NewTimesheetForm(request.POST or None)
    message = None

    if request.method == 'POST' and form.is_valid():
        employee = form.cleaned_data['employee'].strip()
        project_name = form.cleaned_data['project_name'].strip()
        hours_week = form.cleaned_data['hours_week']

        last_week = Timesheet.objects.filter(employee__iexact=employee).aggregate(
            Max('week_number')
        )['week_number__max'] or 0

        if last_week >= 54:
            message = 'This employee already has hours logged for all 54 weeks.'
        else:
            Timesheet.objects.create(
                employee=employee,
                project_name=project_name,
                week_number=last_week + 1,
                hours_week=hours_week,
            )
            return redirect('dashboard')

    selected_employee = request.GET.get('employee', 'all')
    start_month = int(request.GET.get('start_month', 1))
    end_month = int(request.GET.get('end_month', 12))
    if start_month < 1:
        start_month = 1
    if end_month > 12:
        end_month = 12
    if end_month < start_month:
        end_month = start_month

    employee_choices = ['all'] + list(
        Timesheet.objects.order_by('employee')
        .values_list('employee', flat=True)
        .distinct()
    )

    entries = Timesheet.objects.all()
    if selected_employee != 'all':
        entries = entries.filter(employee__iexact=selected_employee)

    projects = sorted(entries.values_list('project_name', flat=True).distinct())

    month_hours = {project: [0] * 12 for project in projects}
    for entry in entries:
        month_index = WEEK_TO_MONTH.get(entry.week_number, 1) - 1
        month_hours[entry.project_name][month_index] += float(entry.hours_week)

    months = MONTH_NAMES[start_month - 1:end_month]
    datasets = []
    for project in projects:
        data = month_hours[project][start_month - 1:end_month]
        datasets.append({
            'label': project,
            'data': data,
            'backgroundColor': f'rgba({hash(project) % 256}, {(hash(project) // 256) % 256}, {(hash(project) // 65536) % 256}, 0.6)',
            'borderColor': 'transparent',
            'borderWidth': 1,
        })

    datasets.append({
        'label': 'Planned Hours',
        'data': [40] * len(months),
        'type': 'line',
        'borderColor': 'rgba(220, 53, 69, 0.9)',
        'borderWidth': 2,
        'fill': False,
        'pointRadius': 3,
        'pointBackgroundColor': 'rgba(220, 53, 69, 0.9)',
    })

    chart_data = {
        'labels': months,
        'datasets': datasets,
    }

    table_data = {}
    for entry in Timesheet.objects.all():
        row = table_data.setdefault(entry.employee, [None] * 54)
        if 1 <= entry.week_number <= 54:
            row[entry.week_number - 1] = entry.hours_week

    return render(
        request,
        'dashboard.html',
        {
            'form': form,
            'message': message,
            'table_data': table_data,
            'week_headers': range(1, 55),
            'chart_data_json': json.dumps(chart_data),
            'employee_choices': employee_choices,
            'selected_employee': selected_employee,
            'start_month': start_month,
            'end_month': end_month,
            'month_choices': list(enumerate(MONTH_NAMES, start=1)),
        },
    )

class LoginPageView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')

class TimesheetUpdateView(UpdateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'edit_timesheet.html'
    success_url = reverse_lazy('dashboard')

class TimesheetDeleteView(DeleteView):
    model = Timesheet
    template_name = 'delete_timesheet.html'
    success_url = reverse_lazy('dashboard')



