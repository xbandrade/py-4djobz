# Generated by Django 4.2.3 on 2023-07-09 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_companyprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyprofile',
            old_name='company_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='companyprofile',
            old_name='company_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='companyprofile',
            old_name='company_website',
            new_name='website',
        ),
    ]
