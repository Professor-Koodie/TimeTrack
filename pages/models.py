from django.db import models

# Create your models here.
class Timesheet(models.Model):
    employee = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, default='General')
    week_number = models.PositiveSmallIntegerField()
    hours_week = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('employee', 'week_number')
        ordering = ['employee', 'week_number']
        indexes = [models.Index(fields=['employee'])]

    def __str__(self):
        return f"{self.employee} - {self.project_name} week {self.week_number}: {self.hours_week} hours"
