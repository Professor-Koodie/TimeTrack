from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_timesheet_task_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timesheet',
            unique_together=None,
        ),
    ]
