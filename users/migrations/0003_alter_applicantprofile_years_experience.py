# Generated by Django 4.2.3 on 2023-07-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_groups_customuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantprofile',
            name='years_experience',
            field=models.IntegerField(default=0),
        ),
    ]