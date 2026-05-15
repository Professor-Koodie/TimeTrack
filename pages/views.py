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

WEEK_MONTH_THRESHOLDS = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52] 

PROJECT_DISPLAY_MAP = {
    'DBN_Maziya': 'DBN Maziya',
    'JHB_Bram': 'JHB Bram',
    'Western_Cape': 'Western Cape',
    'Richards_Bay': 'Richards Bay',
    'Cato_Ridge': 'Cato Ridge',
    'Vandyksdrift_Level_Crossing': 'Vandyksdrift Level Crossing',
    'General_Admin': 'General Admin', 
}


def normalize_project_key(name):
    return name.strip().replace('_', ' ').lower()


def get_project_display(name):
    return PROJECT_DISPLAY_MAP.get(name, name.replace('_', ' '))


def week_number_to_month(week_number):
    for month_index, max_week in enumerate(WEEK_MONTH_THRESHOLDS, start=1):
        if week_number <= max_week:
            return month_index
    return 12


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
        week_number = form.cleaned_data.get('week_number')
        hours_week = form.cleaned_data['hours_week']

        last_week = Timesheet.objects.filter(employee__iexact=employee).aggregate(
            Max('week_number')
        )['week_number__max'] or 0

        if week_number is None:
            if last_week >= 52:
                message = 'This employee already has hours logged for all 52 weeks.'
            else:
                week_number = last_week + 1
        else:
            if week_number < 1 or week_number > 52:
                message = 'Week number must be between 1 and 52.'

        if message is None:
            if Timesheet.objects.filter(employee__iexact=employee, week_number=week_number).exists():
                message = f'Week {week_number} already exists for {employee}.'
            else:
                Timesheet.objects.create(
                    employee=employee,
                    project_name=project_name,
                    week_number=week_number,
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

    project_display = {}
    project_order = []
    for raw_project in entries.values_list('project_name', flat=True):
        key = normalize_project_key(raw_project)
        if key not in project_display:
            project_display[key] = get_project_display(raw_project)
            project_order.append(key)

    month_hours = {project_key: [0] * 12 for project_key in project_order}

    for entry in entries:
        project_key = normalize_project_key(entry.project_name)
        if project_key not in month_hours:
            project_display[project_key] = get_project_display(entry.project_name)
            month_hours[project_key] = [0] * 12
            project_order.append(project_key)

        month_index = week_number_to_month(entry.week_number) - 1
        if 0 <= month_index < 12:
            month_hours[project_key][month_index] += float(entry.hours_week)

    months = MONTH_NAMES[start_month - 1:end_month]
    datasets = []
    for project_key in project_order:
        data = month_hours[project_key][start_month - 1:end_month]
        if any(value != 0 for value in data):
            datasets.append({
                'label': project_display[project_key],
                'data': data,
                'backgroundColor': f'rgba({hash(project_key) % 256}, {(hash(project_key) // 256) % 256}, {(hash(project_key) // 65536) % 256}, 0.6)',
                'borderColor': 'transparent',
                'borderWidth': 1,
            })

    datasets.append({
        'label': 'Planned Hours',
        'data': [160] * len(months),
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
        row = table_data.setdefault(entry.employee, [None] * 52)
        if 1 <= entry.week_number <= 52:
            row[entry.week_number - 1] = entry.hours_week

    return render(
        request,
        'dashboard.html',
        {
            'form': form,
            'message': message,
            'table_data': table_data,
            'week_headers': range(1, 53),
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



