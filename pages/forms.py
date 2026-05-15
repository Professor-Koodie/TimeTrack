from django import forms
from .models import Timesheet

PROJECT_CHOICES = [
    ('DBN_Maziya', 'Durban_Maziya'),
    ('JHB_Bram', 'Johannesburg_Bram'),
    ('Western_Cape', 'Western_Cape'),
    ('Richards_Bay', 'Richards_Bay'), 
    ('Cato_Ridge', 'Cato Ridge'), 
    ('Vandyksdrift_Level_Crossing', 'Vandyksdrift Level Crossing'),
    ('General_Admin', 'General Admin'),
]

class NewTimesheetForm(forms.Form):
    employee = forms.CharField(max_length=100, label='Employee Name')
    project_name = forms.ChoiceField(choices=PROJECT_CHOICES, label='Project', required=True)
    hours_week = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        label='Hours per week'
    )

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['employee', 'project_name', 'week_number', 'hours_week']
