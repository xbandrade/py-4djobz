# Generated by Django 4.2.3 on 2023-07-10 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_application_created_date_job_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='created_date',
            new_name='applied_date',
        ),
    ]