# Generated by Django 4.2.3 on 2023-07-09 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_job_job_finished_alter_application_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job_finished',
            new_name='is_finished',
        ),
    ]