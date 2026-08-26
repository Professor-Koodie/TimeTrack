from django import forms
from .models import Timesheet

PROJECT_CHOICES = [
    ('DBN_Maziya', 'Durban_Maziya'),
    ('JHB_Bram', 'Johannesburg_Braam'),
    ('Western_Cape', 'Western_Cape'),
    ('Richards_Bay', 'Richards_Bay'), 
    ('N3_Cato_Ridge', 'N3_Cato_Ridge'), 
    ('Vandyksdrift_Level_Crossing', 'Vandyksdrift Level Crossing'),
    ('General_Admin', 'General Admin'),
    ('Leave', 'Leave'),
    ('Public_Holiday', 'Public Holiday'),
    ('PT_Platform_Rectification_Gauteng', 'PT Platform Rectification Gauteng'),
    ('Midway_Washaway', 'Midway Washaway'),
    ('QMS', 'QMS'),
    ('Witbank_Level_Crossing', 'Witbank Level Crossing'),
    ('Gautrain_Ballast_Investigation', 'Gautrain Ballast Investigation'),
    ('Bramfontein_Yard', 'Bramfontein Yard'),
    ('PT_Rectification_Western_Cape', 'PT Rectification Western Cape'),
    ('SuperSites', 'Super Sites'),
    ('Valterra_Trek_Scale', 'Valterra Trek Scale'),
    ('Sedra_Edilon', 'Sedra Edilon'),
    ('Tsiko_LTA', 'Tsiko LTA'),  
    ('Iron_Ore', 'Iron Ore'),
    ('RBM_Maintanance', 'RBM Maintanance'),
    ('COTC', 'COTC'),
    ('Bayvue_Rail_Yard', 'Bayvue Rail Yard'),  
    ('MMSEZ', 'MMSEZ'), 
     
]
Task_Description =[
    ('Design', 'Design'),
    ('Draawings', 'Drawings'),
    ('Update_Designs', 'Update Designs'),
    ('Site_Visit', 'Site Visit'),
    ('General_Admin', 'General Admin'),
    ('Submission', 'Submission'),
    ('Client_Review', 'Client Review'), 
    ('Report_Consolidation', 'Report Consolidation'),
    ('Other', 'Other'),

] 

class NewTimesheetForm(forms.Form):
    employee = forms.CharField(max_length=100, label='Employee Name')
    project_name = forms.ChoiceField(choices=PROJECT_CHOICES, label='Project', required=True)
    task_description = forms.ChoiceField(choices=Task_Description, label='Task Description', required=True) #adited
    week_number = forms.IntegerField(
        min_value=1,
        max_value=52,
        required=False,
        label='Week Number (1-52, optional)'
    )
    hours_week = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        label='Hours per week'
    )

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['employee', 'project_name', 'task_description', 'week_number', 'hours_week']
